import abc


class Error:
    @abc.abstractmethod
    def check(self, errors):
        """Check if the given errors are known.

        One class per known type of error should be implemented.

        Args:
            errors (str): The stderr output of the build command.

        Returns:
            ``True`` if the build failure is a known by this class, ``False``
            otherwise.
        """

        return False


class ContainsError(Error):
    """Checks if the errors contain a specific keyword."""

    @property
    @abc.abstractproperty
    def keyword(self):
        """The keyword to check for which to check."""

        return ""

    def check(self, errors):
        return self.keyword in errors


class NotDeclared(ContainsError):
    """When a function is not available at compile time.

    This occurs most often when Blind HELIX identifies an exported symbol that
    is not included in the header files shipped by the library.
    """

    keyword = "was not declared in this scope"


class UndefinedReference(ContainsError):
    """When a function is not available at link time.

    This occurs most often when the library is either split into multiple
    library files (currently unsupported) or when the library statically links
    against another library that it has included in its source/build and that
    produces another library file.
    """

    keyword = "undefined reference to"


types = [NotDeclared, UndefinedReference]


def known(errors):
    """Determine if a given failure is of a known error class.

    This function allows us to determine, from stderr output in the case of a
    build failure, if that failure was due to a known type of error or
    something we haven't seen before.

    Args:
        errors (str): The stderr output of the build command.

    Returns:
        ``True`` if the build failure is a known type, ``False`` otherwise.
    """

    for error in types:
        e = error()

        if e.check(errors):
            return True

    return False
