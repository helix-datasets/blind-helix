import os
import sys
import abc
import json
import argparse
import tempfile
import itertools
import subprocess
import multiprocessing

import tlsh
import pyLZJD


def find(name, environment=None, guess=None):
    """Finds a particular binary on this system.

    Attempts to find the binary given by ``name``, first checking the value of
    the environment variable named ``environment`` (if provided), then by
    checking the system path, then finally checking hardcoded paths in
    ``guess`` (if provided). This function is cross-platform compatible - it
    works on Windows, Linux, and Mac. If there are spaces in the path found,
    this function will wrap its return value in double quotes.

    Args:
        name (str): Binary name.
        environment (str): An optional environment variable to check.
        guess (iterable): An optional list of hardcoded paths to check.

    Returns:
        A string with the absolute path to the binary if found, otherwise
        ``None``.
    """

    def sanitize(path):
        quotes = ("'", "'")
        if " " in path and path[0] not in quotes and path[-1] not in quotes:
            path = '"{}"'.format(path)

        return path

    if environment:
        path = os.environ.get(environment)
        if path is not None:
            path = os.path.abspath(os.path.expanduser(path))
            if os.path.isfile(path):
                return sanitize(path)

    if os.name == "posix":
        search = "which"
    elif os.name == "nt":
        search = "where.exe"
    else:
        raise EnvironmentError("unknown platform: {}".format(os.name))

    try:
        with open(os.devnull, "w") as output:
            path = subprocess.check_output([search, name], stderr=output).decode(
                "utf-8"
            )

        return sanitize(os.path.abspath(path.strip()))
    except subprocess.CalledProcessError:
        pass

    if guess:
        for path in guess:
            if os.path.isfile(path):
                return sanitize(path)

    return None


def run(cmd, cwd=None, exception=None, propagate=False, stdout=None, stderr=None):
    """Run the given command as a subprocess.

    This function caputres ``stdout`` and ``stderr`` by default and returns
    them, and raises the given exception if the process fails.

    Args:
        cmd (str): The command to run.
        cwd (str): The working directory in which to run the command.
        exception: An exception to raise if the command fails.
        propagate (bool): If ``True``, command output will be written to stdout
            and stderr of the current process, otherwise command output is
            captured and returned (and written to ``stdout`` and ``stderr`` if
            provided). Default: ``False``.
        stdout (file): An open file-like object or fileno where stdout should
            be written or ``None``.
        stderr (file): An open file-like object or fileno where stderr should
            be written or ``None``.

    Returns:
        Output to stdout and stderr as binary strings.

    Note:
        Without adding sufficient complexity (additional threads) output cannot
        be both captured and printed stdout/stderr of the current process in
        real time. If this is called with ``propagate=True``, then no output
        will be returned or written to the provided ``stdout``/``stderr``
        arguments.
    """

    cwd = cwd or os.path.abspath(".")

    process = subprocess.run(
        cmd,
        cwd=cwd,
        shell=True,
        stdout=None if propagate else subprocess.PIPE,
        stderr=None if propagate else subprocess.PIPE,
    )

    if stdout and process.stdout:
        stdout.write(process.stdout)
        stdout.flush()
    if stderr and process.stderr:
        stderr.write(process.stderr)
        stderr.flush()

    if process.returncode != 0:
        if exception:
            raise exception
        raise subprocess.CalledProcessError(cmd=cmd, returncode=process.returncode)

    return process.stdout, process.stderr


class Metric(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def binary(self):
        """The name of the metric binary to run."""

        return ""

    @property
    def guess(self):
        """An optional list of hardcoded paths to search for the binary."""

        return []

    @property
    def tool(self):
        """Finds the binary for this metric.

        Raises exceptions if it cannot be found.

        Returns:
            The path to the target binary.
        """

        return find(
            self.binary, environment=f"{self.binary.upper()}_PATH", guess=self.guess
        )

    def preprocess(self, target):
        """Preprocess target files.

        This optional method is called on each file and can include some
        preprocessing of the file prior to actually running the binary. By
        default this does nothing and returns the given path.

        Note:
            If your implementation of this method makes use of tempfiles, be
            sure to save them on this class or they may be deleted before they
            can be used.

        Args:
            target (str): The path to a file that should be preprocessed.

        Returns:
            A path to a processed version of the file.
        """

        return target

    @abc.abstractmethod
    def compare(self, first, second):
        """Compare two files.

        This method is called with the path to two files which have been
        ``preprocess()``'d. It should return a similarity score between 0 and
        1, higher is more similar. This method can make use of the `tool`
        property to get the full path to the target binary.

        Args:
            first (str): A path to a file.
            second (str): A path to a file.

        Returns:
            A similarity score.
        """

        return 0

    def run(self, first, second):
        """Preprocess and compare two files.

        Args:
            first (str): A path to a file.
            second (str): A path to a file.

        Returns:
            A similarity score.
        """

        first, second = [self.preprocess(f) for f in [first, second]]

        return self.compare(first, second)


class SSDeep(Metric):
    binary = "ssdeep"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._temp = []

    def preprocess(self, target):
        processed = tempfile.NamedTemporaryFile()
        self._temp.append(processed)

        run(f"{self.tool} -b {target} > {processed.name}")

        return processed.name

    def compare(self, first, second):
        result, _ = run(f"{self.tool} -k {first} {second} -a")

        score = int(result.decode("utf-8").split()[-1][1:-1]) / 100.0

        return score


class SDHash(Metric):
    binary = "sdhash"
    guess = ["/opt/sdhash/sdhash"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._temp = []

    def preprocess(self, target):
        processed = tempfile.NamedTemporaryFile()
        self._temp.append(processed)

        run(f"{self.tool} {target} > {processed.name}")

        return processed.name

    def compare(self, first, second):
        output, _ = run(f"{self.tool} -c {first} {second} -t 0")

        output = output.decode("utf-8").strip()
        similarity = int(output.split("|")[-1]) / 100.0

        return similarity


class TLSH(Metric):
    binary = "tlsh"

    @staticmethod
    def normalize(score):
        """Normalize a TLSH score on a scale of 0-1.

        Normalization is done using the range selected in the original TLSH
        paper. Here, scores of around 70 give the optimial rate of false
        positives vs detection, so 70 is normalized to 0.5. Scores less than 10
        are normalized to 1 and scores greater than 130 are normalized to 0.
        This is done linearly.
        """

        mid = 70
        minimum = 10
        maximum = mid + (mid - minimum)
        score_range = maximum - minimum

        if score < minimum:
            return 1

        if score > maximum:
            return 0

        return 0.5 - (score - mid) / score_range

    def preprocess(self, target):
        with open(target, "rb") as f:
            h = tlsh.hash(f.read())

        return h

    def compare(self, first, second):
        score = tlsh.diff(first, second)

        return self.normalize(score)


class LZJD(Metric):
    binary = "lzjd"

    def preprocess(self, target):
        return pyLZJD.digest(target)

    def compare(self, first, second):
        return pyLZJD.sim(first, second)


class BinDiff(Metric):
    binary = "bindiff"
    guess = ["/opt/bindiff/bin/bindiff"]

    EXPORT = """#include<idc.idc>
static main() {
    Message("Bindiff Script\\n");
    Batch(0);
    Wait();
    RunPlugin("binexport1164", 2);
    Exit(0);
}"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._temp = []

    def preprocess(self, target):
        idb = tempfile.NamedTemporaryFile()

        binexport = tempfile.NamedTemporaryFile()
        self._temp.append(binexport)

        ida = find(
            "idat64", environment="IDAT64_PATH", guess=["/opt/idapro-7.4/idat64"]
        )

        os.environ["TVHEADLESS"] = "1"
        run(f"{ida} -o{idb.name} -B {target}")

        script = tempfile.NamedTemporaryFile()

        script.write(self.EXPORT.encode("utf-8"))
        script.flush()

        run(f"{ida} -A -S{script.name} -OBinExportModule:{binexport.name} {idb.name}")

        return binexport.name

    def compare(self, first, second):
        bindiff = find(
            "bindiff", environment="BINDIFF_PATH", guess=["/opt/bindiff/bin/bindiff"]
        )

        working = tempfile.TemporaryDirectory()

        output, _ = run(
            f"{bindiff} --primary={first} --secondary={second} --output_dir={working.name}"
        )

        output = output.decode("utf-8").strip()
        similarity = float(output.split("\n")[-2].split()[1][:-1]) / 100

        return similarity


METRICS = [SSDeep, SDHash, TLSH, LZJD, BinDiff]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="run pairwise metrics over a collection of binaries"
    )

    metrics = {m.__name__.lower(): m for m in METRICS}

    parser.add_argument("metric", choices=metrics, help="metric to use")
    parser.add_argument(
        "files", nargs="+", help="one or more files to compare pairwise", type=str
    )

    parser.add_argument("-o", "--output", help="output file (default: stdout)")
    parser.add_argument(
        "-n",
        "--number-workers",
        metavar="WORKERS",
        type=int,
        default=os.cpu_count(),
        help="number of parallel workers to use (default: <cound(CPUs)>)",
    )

    arguments = parser.parse_args()

    files = [os.path.abspath(os.path.expanduser(f)) for f in arguments.files]

    print(
        f"processing {len(files)} files with {arguments.number_workers} workers using metric {arguments.metric}"
    )

    persist = []

    def preprocess(target):
        metric = metrics[arguments.metric]()
        persist.append(metric)

        value = metric.preprocess(target)

        print(f"[+] {arguments.metric} preprocessed {os.path.basename(target)}")

        return (target, value)

    def similarity(pair):
        (first, vfirst), (second, vsecond) = pair

        metric = metrics[arguments.metric]()
        similarity = metric.compare(vfirst, vsecond)

        print(
            f"[+] {arguments.metric} {os.path.basename(first)} vs {os.path.basename(second)}: {similarity}"
        )

        return {
            "first": os.path.basename(first),
            "second": os.path.basename(second),
            "similarity": similarity,
        }

    preprocessed = []
    if arguments.number_workers == 1:
        for f in files:
            preprocessed.append(preprocess(f))
    else:
        with multiprocessing.Pool(arguments.number_workers) as pool:
            preprocessed = pool.map(preprocess, files)

    combinations = itertools.combinations(preprocessed, 2)

    results = []
    if arguments.number_workers == 1:
        for p in combinations:
            results.append(similarity(p))
    else:
        with multiprocessing.Pool(arguments.number_workers) as pool:
            results = pool.map(similarity, combinations)

    del persist

    if arguments.output:
        output = open(arguments.output, "w")
    else:
        output = sys.stdout

    json.dump(results, output)

    print()
    print("complete")
