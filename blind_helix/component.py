import abc
import tempfile

from helix import component
from helix import utils


class LibrarySliceComponent(component.Component):
    """A component generated from a library function.

    This component includes a single exported function from a given library and
    the entire call subgraph based at that function.
    """

    type = "library-slice"

    blueprints = ["cmake-cpp"]

    @property
    @abc.abstractmethod
    def library(self):
        """The name of the library to which this component belongs."""

        return ""

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


__all__ = ["LibrarySliceComponent"]
