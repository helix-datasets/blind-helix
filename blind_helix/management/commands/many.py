import os
import logging
import multiprocessing

from helix.management import utils as management_utils

from ... import parsers
from ... import utils
from ... import exceptions

from . import utils as command_utils


def initialize(lset):
    global lock
    lock = lset


def process(parser, library, working, level):
    path = os.path.join(working, library)

    if not os.path.isdir(path):
        os.makedirs(path)

    if os.path.isfile(os.path.join(path, "succeeded")):
        print(
            "{} {} parsed previously".format(
                utils.color(library, utils.COLOR.BOLD),
                utils.color("✓", utils.COLOR.GREEN),
            )
        )
        return
    elif os.path.isfile(os.path.join(path, "failed")):
        print(
            "{} {} parsed previously".format(
                utils.color(library, utils.COLOR.BOLD),
                utils.color("✗", utils.COLOR.RED),
            )
        )
        return

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logfile = os.path.join(path, "{}.log".format(library))

    command_utils.touch(logfile)

    logging.basicConfig(
        format="[%(levelname)s %(asctime)s %(process)d]: %(message)s",
        filename=logfile,
        level=level,
    )
    logger = logging.getLogger()

    try:
        with lock:
            parsed = parser(library)

        Library = parsed.build()
        TestedLibrary = parsed.test(Library)

        if len(TestedLibrary.functions) == 0:
            raise exceptions.BlindHELIXException(
                "found components in {} but none of them work".format(library)
            )

        with open(os.path.join(path, "{}.bhlx".format(library)), "w") as f:
            TestedLibrary.save(f)
    except exceptions.BlindHELIXException as e:
        print(
            "{} {} {}".format(
                utils.color(library, utils.COLOR.BOLD),
                utils.color("✗", utils.COLOR.RED),
                e,
            )
        )
        logger.critical(e)

        command_utils.touch(os.path.join(path, "failed"))
    else:
        print(
            "{} {} {}/{} ({})".format(
                utils.color(library, utils.COLOR.BOLD),
                utils.color("✓", utils.COLOR.GREEN),
                len(TestedLibrary.functions),
                len(Library.functions),
                utils.color(
                    "{:.2%}".format(
                        len(TestedLibrary.functions) / len(Library.functions)
                    ),
                    utils.COLOR.BOLD,
                ),
            )
        )

        command_utils.touch(os.path.join(path, "succeeded"))


class Command(management_utils.CommandBase):
    """Parse many libraries into sets of Blind HELIX Components.

    Note:
        This command only supports parsers that can automatically locate
        library files given only a library name.
    """

    name = "parse-many"
    help = "parse many libraries into sets of Blind HELIX Components"

    def add_arguments(self, parser):
        self.choices = {}
        for p in parsers.__all__:
            cls = getattr(parsers, p)
            self.choices[cls.display] = cls

        parser.add_argument(
            "parser",
            type=str,
            choices=self.choices,
            help="the name of the Blind HELIX parser to use",
        )

        parser.add_argument(
            "output",
            type=str,
            help="output directory where components should be written",
        )

        parser.add_argument(
            "library", type=str, nargs="+", help="one or more library names"
        )

        parser.add_argument(
            "-n",
            "--number-workers",
            metavar="WORKERS",
            type=int,
            default=round(os.cpu_count() / 2),
            help="number of parallel workers to use (default: <count(CPUs)/2>)",
        )

        parser.add_argument(
            "-v", "--verbose", action="store_true", help="enable verbose logging"
        )

    def handle(self, *args, **options):
        multiprocessing.set_start_method("spawn")

        parser = self.choices[options["parser"]]
        output = command_utils.directory(options["output"])
        level = logging.DEBUG if options["verbose"] else logging.INFO
        lock = multiprocessing.Lock()
        libraries = [
            (parser, lib, output, level) for lib in sorted(set(options["library"]))
        ]

        print(
            "parsing {} libraries with {} workers{}".format(
                utils.color(len(libraries), utils.COLOR.BOLD),
                utils.color(options["number_workers"], utils.COLOR.BOLD),
                " (verbose)" if options["verbose"] else "",
            )
        )

        with multiprocessing.Pool(
            options["number_workers"], initializer=initialize, initargs=(lock,)
        ) as pool:
            pool.starmap(process, libraries)
