import io
import os
import abc
import json
import logging
import tempfile
from datetime import datetime
import base64

from helix import component as helix_component
from helix import exceptions as helix_exceptions

from . import component
from . import errors
from . import exceptions
from . import utils

logger = logging.getLogger()


def build(name, library, functions, included=None, version=None, date=None):
    """Factory to generate a Library class.

    Args:
        name (str): The library name.
        library (str): A path to the library file.
        functions (list): A list of function names in this library.
        version (string): An optional version string given to the generated
            Components - default: "1.0.0".
        date (string): An optional date string given to the generated
            Components - default: the current date.

    Returns:
        A Library generated from the given parameters.
    """

    _name = name
    _library = Library.read(library)
    _functions = functions
    _included = included or {}
    _version = version or "1.0.0"
    _date = date or datetime.now().strftime(component.LibrarySliceComponent.DATE_FORMAT)

    class LibraryInstance(Library):
        name = _name
        version = _version
        date = _date

        library = _library
        functions = _functions
        included = _included

    LibraryInstance.__name__ = "{}{}".format(name.title(), Library.__name__)

    return LibraryInstance


class Library(metaclass=abc.ABCMeta):
    """A collection of Components encapsulated in a portable class.

    Libraries are made portable by storing required files as strings in the
    class itself that can be rewritten to disk as necessary.
    """

    @property
    @abc.abstractmethod
    def name(self):
        return ""

    @property
    @abc.abstractmethod
    def version(self):
        return ""

    @property
    @abc.abstractmethod
    def date(self):
        return ""

    @property
    @abc.abstractmethod
    def library(self):
        return ""

    @property
    @abc.abstractmethod
    def functions(self):
        return []

    @property
    def included(self):
        """A mapping of function names to included functions.

        This is optional but improves sample labeling if provided.
        """

        return {}

    @staticmethod
    def write(content, filename=None):
        """Generates a tempfile with the given content.

        Args:
            content (str): Content to be written to the tempfile - typically
                generated with ``read()``.
            filename (str): Optional file name to write to if you don't want a
                temporary file.

        Returns:
            A tempfile with the given content.
        """

        content = base64.b64decode(content)

        if filename:
            generated = open(filename, "w+b")
        else:
            generated = tempfile.NamedTemporaryFile()

        generated.write(content)

        generated.flush()
        generated.seek(0)

        return generated

    @staticmethod
    def read(path):
        """Loads content from a given file.

        Args:
            path (str): The full path to the file from which to read.

        Returns:
            A string representation of the content of the given file - this is
            typically to be used with ``write()`` to reconstitute the file
            later.
        """

        path = os.path.abspath(os.path.expanduser(path))

        with open(path, "rb") as f:
            content = f.read()

        content = base64.b64encode(content).decode("utf-8")

        return content

    def __init__(self):
        self._library = self.write(self.library)

    @property
    def components(self):
        """Generates the Component classes for this Library.

        Returns:
            A list of Component classes for each of the functions in this
            library.
        """

        components = []

        for _function in self.functions:

            _included = self.included.get(_function, [])

            tags = [
                ("function", "{}-{}".format(self.name, f))
                for f in _included + [_function]
            ]
            tags.append(("library", self.name))
            tags.append(("type", "library-slice"))
            _tags = set(tags)

            class Component(component.LibrarySliceComponent):
                name = "{}-{}".format(self.name, _function)
                verbose_name = name
                version = self.version
                description = "The {} function from the {} library.".format(
                    _function, self.name
                )
                date = self.date
                tags = _tags

                library = self.name
                path = self._library.name
                _library = self._library
                function = _function
                included = _included

            Component.__name__ = "{}{}{}".format(
                self.name, _function.title().replace("_", ""), Component.__name__
            )

            components.append(Component)

        return components

    def test(self, callback=None):
        """Tests all of the functions in this Library.

        Args:
            callback (function): An optional function called with the path to
                each successfully built Component's name and build artifact(s).

        Returns:
            A new Library consisting of only functions that successfully built
            as Components.

        Note:
            This function can take a long time - status updates are logged to
            the standard python logger.
        """

        success = []
        components = self.components

        for i, c in enumerate(components):

            def status(message, level=logging.DEBUG):
                logger.log(
                    level,
                    "({}/{}) {}:{} {} ".format(
                        utils.color(i + 1, utils.COLOR.LIGHT_GREY, stream=logger),
                        utils.color(
                            len(components), utils.COLOR.LIGHT_GREY, stream=logger
                        ),
                        utils.color(c.library, utils.COLOR.BOLD, stream=logger),
                        c.function,
                        message,
                    ),
                )

            options = {"stdout": io.BytesIO(), "stderr": io.BytesIO()}

            try:
                succeeded = True
                working, artifacts = c.test(**options)
            except helix_exceptions.BuildFailure:
                succeeded = False
                options["stderr"].seek(0)
                stderr = options["stderr"].read().decode("utf-8").strip("\n")

                if not errors.known(stderr):
                    raise exceptions.UnexpectedBuildFailure(
                        "build failed in an unexpected way", errors=stderr
                    )
            finally:
                options["stdout"].seek(0)
                options["stderr"].seek(0)

                stdout = options["stdout"].read().decode("utf-8").strip("\n")
                stderr = options["stderr"].read().decode("utf-8").strip("\n")

                if stdout:
                    logger.debug(utils.color(stdout, utils.COLOR.GREY, stream=logger))
                if stderr:
                    logger.debug(utils.color(stderr, utils.COLOR.GREY, stream=logger))

            if succeeded:
                if callback:
                    callback(c.function, artifacts)

                success.append(c.function)
                status(
                    utils.color("✓", utils.COLOR.GREEN, stream=logger),
                    level=logging.INFO,
                )
            else:
                status(
                    utils.color("✗", utils.COLOR.RED, stream=logger), level=logging.INFO
                )

        class LibraryInstance(Library):
            name = self.name
            version = self.version
            date = self.date

            library = self.library
            functions = success
            included = self.included

        LibraryInstance.__name__ = self.__class__.__name__

        return LibraryInstance

    @classmethod
    def saves(cls):
        """Save this Library to a string.

        Returns:
            A string serialized version of this class which can be loaded with
            ``loads()``.
        """

        return json.dumps(
            {
                "name": cls.name,
                "version": cls.version,
                "date": cls.date,
                "library": cls.library,
                "functions": cls.functions,
                "included": cls.included,
            }
        )

    @classmethod
    def save(cls, f):
        """Save this Library to a file.

        Args:
            f (file): An open file-like object to which this class should be
                written which can be read with ``load()``.
        """

        f.write(cls.saves())

    @staticmethod
    def loads(string):
        """Load a Library from a string.

        Args:
            library (str): A string representation of a Library generated with
                ``saves()``.

        Returns:
            A Library class loaded from the given string.
        """

        data = json.loads(string)

        class LibraryInstance(Library):
            name = data["name"]
            version = data["version"]
            date = data["date"]

            library = data["library"]
            functions = data["functions"]
            included = data["included"]

        LibraryInstance.__name__ = "{}{}".format(
            data["name"].capitalize(), Library.__name__
        )

        return LibraryInstance

    @staticmethod
    def load(f):
        """Load a Library from a file.

        Args:
            f (file): An open file-like object from which a Library should be
                loaded. The library should have been saved with ``save()``.

        Returns:
            A Library class loaded from the given file.
        """

        return Library.loads(f.read())


class BlindHelixLibraryLoader(helix_component.Loader):
    def load(self, f):
        return Library.load(f)().components
