import pytest

import core.string_utils as su


def test_strip_line():
    res_1 = su.strip_line("    line")
    res_2 = su.strip_line("    line     ")
    res_3 = su.strip_line("line")
    res_4 = su.strip_line("line      ")
    res_5 = su.strip_line(
        """
    line
    """
    )

    assert res_1 == "line"
    assert res_2 == "line"
    assert res_3 == "line"
    assert res_4 == "line"
    assert res_5 == "line"


def test_line_is_not_empty():
    assert su.line_is_not_empty("Line is not empty")
    assert su.line_is_not_empty(".")
    assert su.line_is_not_empty("") == False


def test_make_lines():
    text_1 = """    Sentence one.
    Sentence 2.
    Sentence more. \n\r     Sentence6\n
    
    
    Sentence 7 has a lot of text and should be a separate line also!
    
    """

    res_1 = su.make_lines(text_1)

    assert len(res_1) == 5
    assert res_1[0] == "Sentence one."
    assert res_1[1] == "Sentence 2."
    assert res_1[2] == "Sentence more."
    assert res_1[3] == "Sentence6"
    assert (
        res_1[4] == "Sentence 7 has a lot of text and should be a separate line also!"
    )


def test_sort_lines_asc_default():
    lines_to_sort: list[str] = [
        "date",
        "nectarine",
        "grape",
        "kiwi",
        "Watermelon",
        "apple",
        "cherry",
        "papaya",
        "Banana",
        "mango",
        "elderberry",
        "orange",
        "raspberry",
        "tangerine",
        "fig",
        "lemon",
        "quince",
        "honeydew",
        "strawberry",
    ]

    result: list[str] = su.sort_lines(lines_to_sort)

    assert result == [
        "Banana",
        "Watermelon",
        "apple",
        "cherry",
        "date",
        "elderberry",
        "fig",
        "grape",
        "honeydew",
        "kiwi",
        "lemon",
        "mango",
        "nectarine",
        "orange",
        "papaya",
        "quince",
        "raspberry",
        "strawberry",
        "tangerine",
    ]


def test_sort_lines_desc():
    lines_to_sort: list[str] = [
        "date",
        "nectarine",
        "grape",
        "kiwi",
        "watermelon",
        "apple",
        "cherry",
        "papaya",
        "banana",
        "mango",
        "elderberry",
        "orange",
        "raspberry",
        "tangerine",
        "fig",
        "lemon",
        "quince",
        "honeydew",
        "strawberry",
    ]

    result: list[str] = su.sort_lines(lines=lines_to_sort, order=su.DESC)

    assert result == [
        "watermelon",
        "tangerine",
        "strawberry",
        "raspberry",
        "quince",
        "papaya",
        "orange",
        "nectarine",
        "mango",
        "lemon",
        "kiwi",
        "honeydew",
        "grape",
        "fig",
        "elderberry",
        "date",
        "cherry",
        "banana",
        "apple",
    ]


def test_sort_lines_asc_case_insensitive():
    lines_to_sort: list[str] = [
        "Date",
        "nectarine",
        "grape",
        "kiwi",
        "Watermelon",
        "apple",
        "cherry",
        "papaya",
        "banana",
        "mangO",
        "Elderberry",
        "orange",
        "raspberry",
        "tangerine",
        "fig",
        "Lemon",
        "quince",
        "honeydew",
        "strawberry",
    ]

    result: list[str] = su.sort_lines(lines_to_sort, case_insensitive=True)

    assert result == [
        "apple",
        "banana",
        "cherry",
        "Date",
        "Elderberry",
        "fig",
        "grape",
        "honeydew",
        "kiwi",
        "Lemon",
        "mangO",
        "nectarine",
        "orange",
        "papaya",
        "quince",
        "raspberry",
        "strawberry",
        "tangerine",
        "Watermelon",
    ]


def test_sort_lines_order_exception():
    with pytest.raises(su.SortingOrderIsNotSupportedException) as ex:
        su.sort_lines(["lien1", "line2"], order="non-existing")
    assert str(ex.value) == "Passed order (non-existing) is not supported"


def test_sort_lines_with_incorrect_argument():
    lines = []
    result = su.sort_lines(lines)

    assert lines == result

    assert None is su.sort_lines(None)


def test_join_lines():
    lines_to_join_1 = ["line1", "line2", "line3", "line4", "line5"]
    res_1 = su.join_lines(lines_to_join_1)

    assert res_1 == "line1 line2 line3 line4 line5"

    lines_to_join_2 = ["line1", "line2", "line3", "line4", "line5"]
    res_2 = su.join_lines(lines_to_join_2, separator="&&")

    assert res_2 == "line1&&line2&&line3&&line4&&line5"
