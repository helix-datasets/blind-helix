import os
import copy
import uuid
import json
import shutil
import random
import tempfile
import multiprocessing

from helix import utils as helix_utils
from helix import exceptions
from helix.management import utils as management_utils

from ... import component
from ... import utils

from . import utils as command_utils


class SamplingError(Exception):
    """Raised when there is a problem generating a sample list."""


def generate(components, transforms, output, verbose=False):
    blueprint = helix_utils.load("helix.blueprints", components[0].blueprints[0])

    configured = []
    for specification in transforms:
        specification = helix_utils.parse(specification)
        transform = helix_utils.load("helix.transforms", specification["name"])()

        if transform.type == transform.TYPE_SOURCE:
            raise exceptions.BuildFailure(
                "Blind HELIX does not support source transforms"
            )

        transform.configure(**specification.get("configuration", {}))

        configured.append(transform)

    finalized = []
    for Component in components:
        c = Component()
        c.generate()
        c.finalize()

        finalized.append(c)

    blueprint = blueprint("sample", finalized, configured)

    working = tempfile.TemporaryDirectory()

    (artifact,) = blueprint.build(working.name, options={"propagate": verbose})

    shutil.copy(artifact, output)

    return blueprint.tags


def process(components, transforms, working, verbose=False):
    components = [component.LibrarySliceComponent.loads(c) for c in components]

    name = "[{}]".format(", ".join([c().name for c in components]))
    identifier = uuid.uuid4()

    try:
        tags = generate(
            components,
            transforms,
            os.path.join(working, identifier.hex),
            verbose=verbose,
        )
    except exceptions.BuildFailure as e:
        print(
            "{} {} {}".format(
                name,
                utils.color("✗", utils.COLOR.RED),
                e,
            )
        )

        return {}

    print(
        "{} {} {}".format(
            name,
            utils.color("✓", utils.COLOR.GREEN),
            identifier,
        )
    )

    return {identifier.hex: tags}


def simple(collection, samples=None, components=None):
    """A simple dataset with a single Component per sample.

    Note:
        The number of components per sample requested is ignored by this
        strategy.
    """

    options = [[component] for library in collection.values() for component in library]

    if samples:
        if len(options) < samples:
            raise SamplingError(
                "cannot generate {} samples (maximum {} possible)".format(
                    samples, len(collection)
                )
            )

        return random.sample(options, samples)

    return options


def rand(collection, samples=None, components=None):
    """A completely random dataset.

    May contain exact duplicates or duplicate components in a single build.

    Note:
        This is not a good dataset generation strategy because there may be
        overlaps between individual library functionality that are not
        encapsulated by the dataset labels. See the ``stratified`` strategy
        instead.
    """

    samples = samples or 100
    components = components or 50

    options = []

    for _ in range(samples):
        sample = []
        for _ in range(components):
            library = random.choice(list(collection.keys()))
            component = random.choice(collection[library])

            sample.append(component)

        options.append(sample)

    return options


def stratified_random(collection, samples=None, components=None):
    """A library-stratified randomly generated dataset.

    Generates a dataset where at most one component per library is present in
    each sample and ensures that no exact duplicates are created.

    Note:
        The approach used here was selected after much deliberation over
        potentially more optimal, non-random approaches. As the number of
        samples required gets closer to the maximum number possible to generate
        given the library of components, this becomes more and more
        inefficient. This relies heavily on the library of components being
        reasonably large, relative to the number of samples requested.

        One could also generate all possible combinations and then select from
        them randomly. The problem with this approach is that the number of
        possible combinations for a relatively small library of components is
        far larger than could fit in all of the memory on earth.

        Another potential approach would be to simply take the first ``count``
        combinations generated. The problem is that most algorithms for
        generating subsets of a given size generate them in lexical order which
        results in a bias problem for the generated dataset when any number
        less than the maximum number of samples is generated.
    """

    samples = samples or 100
    components = components or 50

    # TODO check combinatorics for requested count of samples

    options = set()
    for _ in range(samples):
        sample = []

        for _ in range(25):
            libraries = random.sample(list(collection), components)
            for library in libraries:
                sample.append(random.choice(collection[library]))

            sample = tuple(sample)

            if sample not in options:
                break
        else:
            raise Exception(
                "could not generate {} unique random samples: maximum number of tries reached".format(
                    samples
                )
            )

        options.add(sample)

    return list(options)


def stratified_walk(collection, samples=None, components=None):
    """A library-stratified dataset with additional similarity.

    Generates a dataset by randomly replacing a random number of components
    from one build to the next in a library-stratified fashion.
    """

    CHANGE_PERCENT = 0.02
    """The maximum percentage of components that can change.

    Between one sample and the next.
    """

    samples = samples or 100
    components = components or 50

    options = []

    sample = []
    libraries = random.sample(list(collection), components)
    for library in libraries:
        sample.append(random.choice(collection[library]))

    options.append(sample)

    for _ in range(samples - 1):
        count = random.randint(0, round(components * CHANGE_PERCENT))

        for _ in range(count):
            changed = random.randint(0, components - 1)

            library = random.choice(list(collection))
            component = random.choice(collection[library])

            sample[changed] = component

        options.append(copy.deepcopy(sample))

    return options


class Command(management_utils.CommandBase):
    """Generate a dataset from a collection of Blind HELIX Components."""

    name = "dataset"
    help = "generate a dataset from a collection of Blind HELIX Components"

    def add_arguments(self, parser):
        parser.add_argument(
            "strategy",
            type=str,
            choices=["simple", "random", "stratified-random", "stratified-walk"],
            help="dataset generation strategy",
        )

        parser.add_argument(
            "output", type=str, help="output directory where dataset should be written"
        )

        parser.add_argument(
            "export", type=str, nargs="+", help="one or more export files"
        )

        parser.add_argument(
            "-t",
            "--transforms",
            help="transform(s) to apply (by name)",
            nargs="*",
            default=[],
        )

        parser.add_argument(
            "-s",
            "--samples",
            type=int,
            default=None,
            help="number of samples to generate (randomly selected from possible options for the given strategy)",
        )

        parser.add_argument(
            "--maximum-samples",
            type=int,
            default=None,
            help="maximum number of samples to generate",
        )

        parser.add_argument(
            "-c",
            "--components",
            type=int,
            default=None,
            help="number of components per sample (if applicable for the given sample generation strategy)",
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
            "-v", "--verbose", action="store_true", help="build in verbose mode"
        )

    def handle(self, *args, **options):
        if os.path.isdir(options["output"]):
            command_utils.error(
                "output directory {} already exists".format(options["output"])
            )

        output = command_utils.directory(options["output"])

        try:
            _, components = command_utils.load(options["export"])
        except Exception as e:
            command_utils.error(e)

        try:
            if options["strategy"] == "simple":
                strategy = simple
            elif options["strategy"] == "random":
                strategy = rand
            elif options["strategy"] == "stratified-random":
                strategy = stratified_random
            elif options["strategy"] == "stratified-walk":
                strategy = stratified_walk
            else:
                command_utils.error(
                    "invalid sample generation strategy {}".format(
                        utils.color(options["strategy"], utils.COLOR.BOLD)
                    )
                )

            samples = strategy(
                components,
                options.get("samples", None),
                options.get("components", None),
            )
        except SamplingError as e:
            command_utils.error(e)

        print(
            "building {} samples with {} workers".format(
                utils.color(len(samples), utils.COLOR.BOLD),
                utils.color(options["number_workers"], utils.COLOR.BOLD),
            )
        )

        arguments = [
            ([c.saves() for c in s], options["transforms"], output, options["verbose"])
            for s in samples
        ]

        if options["number_workers"] == 1:
            results = [process(*a) for a in arguments]
        else:
            with multiprocessing.Pool(options["number_workers"]) as pool:
                results = pool.starmap(process, arguments)

        results = [r for r in results if r]

        if "maximum_samples" in options:
            results = results[: options["maximum_samples"]]

        labels = {}
        for result in results:
            labels.update(result)

        print(
            "built {} samples in {}".format(
                utils.color(len(labels), utils.COLOR.BOLD),
                utils.color(options["output"], utils.COLOR.BOLD),
            )
        )

        with open(os.path.join(output, "labels.json"), "w") as f:
            json.dump(labels, f)
