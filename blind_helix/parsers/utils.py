import os
import tempfile
import subprocess

from helix import utils as helix_utils

from .. import exceptions


class VCPKGError(exceptions.BlindHELIXException):
    """Errors specific to VCPKG."""


class VCPKGParserMixin:
    """A mixin for using VCPKG for library file location.

    This requires that VCPKG either be installed globally (i.e., ``vcpkg`` is
    in the ``PATH``) or that the user set the ``VCPKG_PATH`` environment
    variable to point ot the ``vcpkg`` binary.

    Note:
        VCPKG is not thread safe any may throw unexpected errors that cause
        parsing to fail if multiple instances of it run at once.
    """

    VCPKG_ENVIRONMENT_VARIABLE = "VCPKG_PATH"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.vcpkg = helix_utils.find(
            "vcpkg", environment=self.VCPKG_ENVIRONMENT_VARIABLE, guess=["/opt/vcpkg/"]
        )

        if self.vcpkg is None:
            raise exceptions.BlindHELIXException(
                "`vcpkg` could not be found - please ensure it is in the system `PATH` or the `{}` environment variable is set".format(
                    self.VCPKG_ENVIRONMENT_VARIABLE
                )
            )

        self._build = tempfile.TemporaryDirectory()

        stdout, _ = helix_utils.run("{} list {}".format(self.vcpkg, self.name))
        if self.name.encode("utf-8") not in stdout:
            stdout, _ = helix_utils.run("{} search {}".format(self.vcpkg, self.name))

            if self.name.encode("utf-8") not in stdout:
                raise VCPKGError("{} is not a valid VCPKG package".format(self.name))
            else:
                raise VCPKGError(
                    "{} is not installed under VCPKG - please install it with `vcpkg install {}` first".format(
                        self.name, self.name
                    )
                )

        try:
            helix_utils.run(
                "{} install --x-install-root {} {}".format(
                    self.vcpkg, self._build.name, self.name
                )
            )
        except subprocess.CalledProcessError:
            raise VCPKGError("failed to run install command on {}".format(self.name))

    def __del__(self):
        if hasattr(self, "_build"):
            self._build.cleanup()

    def _filter_path(self, options):
        """Heuristics for selecting the correct library file.

        Args:
            options (list:str): A list of possible options.

        Returns:
            The selected library file name.

        Note:
            There is actually nothing preventing us from linking against all of
            libraries we find and this would indeed increase the identified
            function yield. However, because VCPKG automatically resolves
            dependencies, there's no way of knowing if the other library files
            actually belong to another package. This could be problematic for
            the data as it would introduce cross-component overlaps that are
            hard to track and quantify.

            Unfortunately this also means that we can't support libraries which
            spread their functionality across multiple library files.
        """

        if len(options) == 0:
            raise VCPKGError(
                "no library file found for {} (note: header-only libraries are not supported)".format(
                    self.name
                )
            )

        if len(options) == 1:
            return options[0]

        filters = [
            lambda o: self.name in o,
            lambda o: o == "lib{}.a".format(self.name),
            lambda o: self.name.split("-")[0] in o,
        ]

        for f in filters:
            test = [o for o in options if f(os.path.basename(o))]

            if len(test) == 1:
                return test[0]

        raise exceptions.BlindHELIXException(
            "multiple library files found for {} - resolution unclear".format(self.name)
        )

    def path(self, name):
        """Locate the main library file using VCPKG.

        Install the package with VCPKG in a temporary install directory where
        it is the only package. Then, select from the generated library files
        according to filtering heuristics (if there are more than one).
        """

        options = []

        vcpkg_install_root = os.path.join(os.path.dirname(self.vcpkg), "installed")

        for root, dirs, files in os.walk(self._build.name):
            if os.path.basename(root) == "lib" and "debug" not in root:
                for name in files:
                    if name.endswith(".a"):
                        install_path = root.split(self._build.name)[-1][1:]
                        options.append(
                            os.path.join(vcpkg_install_root, install_path, name)
                        )

        return self._filter_path(options)
