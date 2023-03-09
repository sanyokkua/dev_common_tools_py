import importlib.resources as res

import core.string_utils as su
import resources


def load_text(file_name: str) -> list[str]:
    text: str = res.read_text(resources, file_name)
    lines: list[str] = su.make_lines(text, separator="\n")
    return lines
