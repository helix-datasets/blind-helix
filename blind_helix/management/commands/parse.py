import sys
import logging

from helix.management import utils as management_utils

from ... import utils
from ... import parsers
from ... import exceptions


def error(exception):
    print(
        "{}: {}".format(
            utils.color("error", utils.COLOR.BOLD, utils.COLOR.RED), exception
        )
    )

    if isinstance(exception, exceptions.UnexpectedBuildFailure):
        print(utils.color(exception.errors, utils.COLOR.GREY))

    exit(1)


class Command(management_utils.CommandBase):
    """Parse a single library into a set of Blind HELIX Components."""

    name = "parse"
    help = "parse a single library into a set of Blind HELIX Components"

    def add_arguments(self, parser):
        self.choices = {}
        for p in parsers.__all__:
            cls = getattr(parsers, p)
            self.choices[cls.display] = cls

        parser.add_argument(
            "parser", type=str, choices=self.choices, help="parser to use"
        )

        parser.add_argument(
            "name",
            help="library name (used for locating the library - must be exact)",
        )

        parser.add_argument(
            "-p",
            "--path",
            default=None,
            help="path to the target library (optional if it can be inferred from the library name)",
        )

        parser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="display build output while testing potential Components",
        )

        parser.add_argument(
            "output", help="output file to write the generated Components"
        )

    def handle(self, *args, **options):
        logging.basicConfig(
            format="%(message)s",
            stream=sys.stdout,
            level=logging.DEBUG if options["verbose"] else logging.INFO,
        )

        Parser = self.choices[options["parser"]]

        print("parsing {}".format(utils.color(options["name"], utils.COLOR.BOLD)))

        try:
            parser = Parser(options["name"], options.get("path", None))
            Library = parser.build()
            TestedLibrary = parser.test(Library)
        except exceptions.BlindHELIXException as e:
            error(e)

        with open(options["output"], "w") as f:
            TestedLibrary.save(f)

        print(
            "saved {} Components to {}".format(
                utils.color(len(TestedLibrary.functions), utils.COLOR.BOLD),
                utils.color(options["output"], utils.COLOR.BOLD),
            )
        )
