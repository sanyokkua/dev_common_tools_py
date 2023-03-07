ASC = "asc"
DESC = "dsc"


def strip_line(line: str) -> str:
    return line.strip()


def line_is_not_empty(line: str) -> bool:
    return len(line) > 0 and len(strip_line(line)) > 0


def make_lines(text: str, separator: str = "\n") -> list[str]:
    result: list[str] = text.split(separator)
    result: list[str] = list(map(strip_line, result))
    result: list[str] = list(filter(line_is_not_empty, result))
    return result


def sort_lines(
    lines: list[str], order: str = ASC, case_insensitive: bool = False
) -> list[str]:
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
    joined: str = separator.join(lines)
    return joined


class SortingOrderIsNotSupportedException(Exception):
    def __init__(self, message: str) -> None:
        Exception.__init__(self, message)
