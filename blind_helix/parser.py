import abc
import shutil
import tempfile

from . import exceptions
from . import library


class LibraryParser(metaclass=abc.ABCMeta):
    """A base class for parsing a list of functions from a library.

    Args:
        name (str): The library name.
        path (str): The full path to the library file (optional if it can be
            inferred from the library name)
    """

    @property
    @abc.abstractmethod
    def display(self):
        """The display name of this parser."""

        return ""

    def __init__(self, name, path=None):
        self.name = name
        self._path = path

    def path(self, name):
        """Find the absolute path to a given library.

        Implement this optional property if you want to support automatic
        library location lookup.

        Args:
            name (str): The name of the library to locate.

        Returns:
            The absolute path to the given library.
        """

        if self._path:
            return self._path

        raise exceptions.LibraryNotFound(
            "cannot automatically find library file - it must be specificed manually via ``path``"
        )

    @abc.abstractmethod
    def parse(self, path, exported=True):
        """Parse the given binary into a list of function names.

        May be called on either an executable or a library file.

        Args:
            path (str): The absolute path to the binary file.
            exported (bool): If ``True`` include only exported functions.

        Returns:
            A list of callable functions in the binary.
        """

        return []

    def finalize(self, library):
        """An optional method for modifying the target library before parsing.

        You can override this method if you want to support, for example,
        ensuring exported functions from the library are unique prior to
        parsing.

        Args:
            library (str): The aboslute path to the library file.

        Returns:
            The modified library file (as a temporary file).
        """

        f = tempfile.NamedTemporaryFile()

        shutil.copyfile(library, f.name)

        return f

    def build(self, version=None, date=None):
        """Generates a Library using this Parser.

        Returns:
            A generated Library, ready for testing/export/component generation.
        """

        finalized = self.finalize(self.path(self.name))

        functions = self.parse(finalized.name)

        return library.build(self.name, finalized.name, functions, version, date)

    def test(self, library):
        """Tests a given Library class.

        Args:
            library (class): A library class.

        Returns:
            A modified version of ``library`` that only includes functioning
            Components.
        """

        finalized = self.finalize(self.path(self.name))
        base = set(self.parse(finalized.name, exported=False))

        included = {}

        def parse(name, artifacts):
            included[name] = []

            for a in artifacts:
                functions = set(self.parse(a, exported=False))
                included[name] += list(functions & base)

        library = library()
        TestedLibrary = library.test(callback=parse)
        TestedLibrary.included = included

        return TestedLibrary
