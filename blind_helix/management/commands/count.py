import statistics

from helix.management import utils as management_utils

from ... import utils

from . import utils as command_utils


class Command(management_utils.CommandBase):
    """Count the number of Components and Libraries in one or more exports."""

    name = "count"
    help = "count the number of Components and Libraries in one or more exports"

    def add_arguments(self, parser):
        parser.add_argument(
            "export", type=str, nargs="+", help="one or more export files"
        )

        parser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="print detailed statistics about the exports",
        )

    def handle(self, *args, **options):
        _, components = command_utils.load(options["export"])
        counts = [len(v) for v in components.values()]

        print(
            "found {} components in {} libraries".format(
                utils.color(sum(counts), utils.COLOR.BOLD),
                utils.color(len(components), utils.COLOR.BOLD),
            )
        )

        if options["verbose"]:
            print(
                "  median number of components per library: {}".format(
                    utils.color(statistics.median(counts), utils.COLOR.BOLD)
                )
            )
