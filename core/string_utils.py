ASC = "asc"
DESC = "dsc"


def strip_line(line: str) -> str:
    """
    Strips a line of leading and trailing whitespace characters.

    :param line: The line to strip.
    :return: The stripped line.
    """
    return line.strip()


def line_is_not_empty(line: str) -> bool:
    """
    Checks if a line is not empty.

    :param line: The line to check.
    :return: True if the line is not empty, False otherwise.
    """
    return len(line) > 0 and len(strip_line(line)) > 0


def make_lines(text: str, separator: str = "\n") -> list[str]:
    """
    Splits a text into lines using the specified separator.

    :param text: The text to split into lines.
    :param separator: The separator to use for splitting. Default is "\n".
    :return: A list of lines.
    """
    result: list[str] = text.split(separator)
    result: list[str] = list(map(strip_line, result))
    result: list[str] = list(filter(line_is_not_empty, result))
    return result


def sort_lines(
    lines: list[str], order: str = ASC, case_insensitive: bool = False
) -> list[str]:
    """
    Sorts a list of lines in ascending or descending order.

    :param lines: The list of lines to sort.
    :param order: The sorting order. Can be either ASC or DESC. Default is ASC.
    :param case_insensitive: Whether to sort case-insensitively. Default is False.
    :return: The sorted list of lines.
    """
    if not lines or len(lines) <= 1:
        return lines
    if order not in [ASC, DESC]:
        raise SortingOrderIsNotSupportedException(
            "Passed order ({}) is not supported".format(order)
        )

    if case_insensitive:
        sorted_strings = sorted(lines, key=str.casefold)
    else:
        sorted_strings = sorted(lines)
    if order == DESC:
        sorted_strings.reverse()
    return sorted_strings


def join_lines(lines: list[str], separator: str = " ") -> str:
    """
    Joins a list of lines into a single string using the specified separator.

    :param lines: The list of lines to join.
    :param separator: The separator to use for joining. Default is " ".
    :return: The joined string.
    """
    joined: str = separator.join(lines)
    return joined


class SortingOrderIsNotSupportedException(Exception):
    """
    An exception that is raised when an unsupported sorting order is passed to the sort_lines function.
    """

    def __init__(self, message: str) -> None:
        """
        Initializes a new instance of the SortingOrderIsNotSupportedException class.

        :param message: The error message.
        """
        Exception.__init__(self, message)
