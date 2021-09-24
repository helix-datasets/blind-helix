import argparse

from . import management


def main():
    parser = argparse.ArgumentParser(
        description="Blind HELIX: Automatic static-only HELIX Component extraction"
    )

    management.build_parser(parser, management.commands)

    args = parser.parse_args()

    args.func(args)


if __name__ == "__main__":
    main()
