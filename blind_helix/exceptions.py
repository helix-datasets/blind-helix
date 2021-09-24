class BlindHELIXException(Exception):
    """The base class for all custom exceptions."""


class LibraryNotFound(BlindHELIXException):
    """Raised when a given library cannot be found."""


class UnexpectedBuildFailure(BlindHELIXException):
    """Raised when a build fails in an unexpected way."""

    def __init__(self, *args, errors, **kwargs):
        super().__init__(*args, **kwargs)

        self.errors = errors
