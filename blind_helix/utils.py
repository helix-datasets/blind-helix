import sys
import logging


class COLOR:
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    LIGHT_GREY = "\033[37m"
    GREY = "\033[90m"

    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    END = "\033[0m"


def _supported(stream):
    """Determines if the given stream supports color.

    Args:
        stream: The target stream object - multiple types are supported here -
            see the code for a full list.

    Returns:
        ``True`` if colors are supported by the target stream and ``False``
        otherwise.
    """

    if hasattr(stream, "isatty"):
        return stream.isatty()
    elif isinstance(stream, logging.Logger):
        for handler in stream.handlers:
            if not handler.stream.isatty():
                return False
        return True

    return False


def color(text, *colors, stream=sys.stdout):
    """Change the given text to the given color, if supported.

    Args:
        text (str): Some text to modify.
        *colors: The color(s) to apply - from the ``COLOR`` class. Multiple
            arguments are allowed to allow for format/color combinations.
        stream (file): (Optional) A file-like object where the output will be
            streamed to detect color support. If not provided, this assumes
            that the output will be written to ``stdout``.

    Returns:
        Transformed text.
    """

    if _supported(stream):
        return "{}{}{}".format("".join(colors), text, COLOR.END)
    else:
        return text
