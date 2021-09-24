import os

from ... import library
from ... import utils


def load(exports):
    libraries = []
    components = {}

    for export in exports:
        with open(os.path.abspath(os.path.expanduser(export)), "r") as f:
            lib = library.Library.load(f)()
            for component in lib.components:
                if component.library not in components:
                    components[component.library] = []

                components[component.library].append(component)

            libraries.append(lib)

    return libraries, components


def error(exception):
    print(
        "{}: {}".format(
            utils.color("error", utils.COLOR.BOLD, utils.COLOR.RED), exception
        )
    )
    exit(1)


def touch(path):
    with open(path, "w") as f:
        f.write("")


def directory(path):
    fullpath = os.path.abspath(os.path.expanduser(path))

    if not os.path.isdir(fullpath):
        try:
            os.makedirs(fullpath)
        except Exception as e:
            error(e)

    return fullpath
