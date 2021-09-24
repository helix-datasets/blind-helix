import os
import tempfile

import magic
import lief

from helix import utils as helix_utils

from .. import parser
from .. import exceptions

from . import utils


lief.logging.disable()


class GenericLinuxLibrary(parser.LibraryParser):
    """A library parser for system-installed Linux libraries."""

    display = "generic-linux-library"

    def _parse_archive(self, archive, callback):
        working = tempfile.TemporaryDirectory()

        ar = helix_utils.find("ar")
        helix_utils.run(
            "{} x {}".format(ar, archive),
            working.name,
            exception=exceptions.BlindHELIXException(
                "invalid library file: {}".format(archive)
            ),
        )

        for unit in os.listdir(working.name):
            if os.path.splitext(unit)[1] != ".o":
                continue

            binary = lief.parse(os.path.join(working.name, unit))

            callback(binary)

        working.cleanup()

    def _parse_executable(self, path, callback):
        binary = lief.parse(path)

        callback(binary)

    def parse(self, path, exported=True):
        """Generates a list of functions in the given binary.

        1. Extracts all object files from the target archive.
        2. Parses object files for "exported" functions.
        3. Returns the list of exported function names.
        """

        functions = []

        def add(binary):
            for s in binary.symbols:
                if not s.is_function or s.imported:
                    continue

                if exported and not s.exported:
                    continue

                name = lief.demangle(s.name)

                if name is not None:
                    # Skipping C++ functions.
                    # Experimentally, C++ functions are somewhat problematic
                    # because they often contain a lot of template code that is
                    # essentially the same across all instances. More experimenting
                    # with C++ functions is necessary before attempting to include
                    # them.

                    continue

                functions.append(s.name)

        with magic.Magic() as m:
            filetype = m.id_filename(path)

        if "ar archive" in filetype:
            self._parse_archive(path, add)
        else:
            self._parse_executable(path, add)

        return functions

    def finalize(self, library):
        """Make exported symbols unique for the given library.

        This uses objcopy to prefix all exported symbols with the library name.
        """

        symbols = []

        def add(binary):
            for e in binary.exported_symbols:
                name = lief.demangle(e.name)

                if name is None:
                    symbols.append(e.name)

                # Skipping C++ symbols.
                # See rationale in the parsing function for more details.

        self._parse_archive(library, add)

        unique = tempfile.NamedTemporaryFile()
        mapping = tempfile.NamedTemporaryFile()

        for symbol in symbols:
            mapping.write(
                "{} {}_{}\n".format(symbol, self.name, symbol).encode("utf-8")
            )

        mapping.flush()
        mapping.seek(0)

        objcopy = helix_utils.find("objcopy")
        helix_utils.run(
            "{} --redefine-syms={} {} {}".format(
                objcopy, mapping.name, library, unique.name
            ),
            exception=exceptions.BlindHELIXException(
                "failed to rewrite the target library"
            ),
        )

        return unique


class VCPKGLinuxLibrary(utils.VCPKGParserMixin, GenericLinuxLibrary):
    display = "vcpkg-linux-library"


__all__ = ["GenericLinuxLibrary", "VCPKGLinuxLibrary"]
