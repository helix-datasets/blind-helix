import abc
import json
import tempfile

from helix import component
from helix import utils


class LibrarySliceComponent(component.Component):
    """A component generated from a library function.

    This component includes a single exported function from a given library and
    the entire call subgraph based at that function.
    """

    @property
    @abc.abstractmethod
    def library(self):
        """The name of the library to which this component belongs."""

        return ""

    @property
    def verbose_library(self):
        """Optional verbose version of the library name."""

        return self.library

    @property
    @abc.abstractmethod
    def path(self):
        """The path to this library file."""

        return ""

    @property
    @abc.abstractmethod
    def function(self):
        """The name of the exported library function."""

        return ""

    """The list of function names included in this Component.

    This is so that additional labels can be applied to the Component for
    each function in the library that appears. This gives a more accurate
    measure of relative sample similarity as there are frequently large
    Component function subgraphs shared across Components in the same
    library.

    This is optional.
    """
    included = []

    @property
    def name(self):
        return "{}-{}".format(self.library, self.function)

    @property
    def verbose_name(self):
        return "{} {}".join(self.verbose_library, self.function)

    @property
    def description(self):
        return "The {} function from the {} library.".format(
            self.function, self.verbose_library
        )

    type = "library-slice"

    @property
    def tags(self):
        tags = set(
            [
                ("library", self.library),
                ("type", "library-slice"),
            ]
        )

        for function in self.included + [self.function]:
            tags.add(("function", "{}-{}".format(self.library, function)))

        return tuple(tags)

    blueprints = ["cmake-cpp"]

    @property
    def libraries(self):
        return [self.path]

    def generate(self):
        self.functions = ["extern void *{};".format(self.function)]
        self.calls = {"main": ["((void (*)()){})();".format(self.function)]}

    @classmethod
    def test(cls, **kwargs):
        """Tests the given Component to ensure that it compiles.

        Build errors are propagated - if this function completes without
        raising an exception and returns nothing then the Component was tested
        successfully.

        Args:
            **kwargs: Can be used to pass build options to the Blueprint's
                ``build()`` method.

        Note:
            This function may take a very long time - if you want status
            updates, set up a logging handler.
        """

        c = cls()
        c.generate()
        c.finalize()

        CMakeCppBlueprint = utils.load("helix.blueprints", cls.blueprints[0])
        b = CMakeCppBlueprint("test", [c])

        working = tempfile.TemporaryDirectory()

        try:
            artifacts = b.build(working.name, options=kwargs)
        except Exception as e:
            working.cleanup()
            raise e

        return working, artifacts

    @classmethod
    def saves(cls):
        """Save this Component to a string.

        Returns:
            A string serialized version of this class which can be loaded with
            ``loads()``.

        Note:
            Components are not necessarily portable - there's no guarantee that
            reloading this saved Component will result in a working Component.
        """

        return json.dumps(
            {
                "library": cls.library,
                "version": cls.version,
                "date": cls.date,
                "path": cls.path,
                "function": cls.function,
                "included": cls.included,
            }
        )

    @staticmethod
    def loads(string):
        """Load a Component from a string.

        Args:
            string (str): A string representation of a Component generated with
                ``saves()``.

        Returns:
            A Component class loaded from the given string.
        """

        data = json.loads(string)

        class ComponentInstance(LibrarySliceComponent):
            library = data["library"]
            version = data["version"]
            date = data["date"]

            path = data["path"]
            function = data["function"]
            included = data["included"]

        return ComponentInstance


__all__ = ["LibrarySliceComponent"]
