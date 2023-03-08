import json


def format_json(json_string: str, indentation: int = 4, sort_keys: bool = True) -> str:
    """
    Formats a JSON string with specified indentation and key sorting.

    :param json_string: The JSON string to format.
    :param indentation: The number of spaces to use for indentation. Default is 4.
    :param sort_keys: Whether to sort the keys in the output. Default is True.
    :return: The formatted JSON string.
    """
    parsed_json = json.loads(json_string)
    formatted_json = json.dumps(parsed_json, indent=indentation, sort_keys=sort_keys)
    return formatted_json


def validate_json(json_string: str) -> str:
    """
    Validates a JSON string and returns an error message if it's invalid.

    :param json_string: The JSON string to validate.
    :return: An error message if the JSON string is invalid, otherwise an empty string.
    """
    try:
        json.loads(json_string)
    except json.JSONDecodeError as e:
        return e.__str__()
    return ""


def flatten_json(json_string: str) -> str:
    """
    Flattens a JSON string by removing all whitespace characters.

    :param json_string: The JSON string to flatten.
    :return: The flattened JSON string.
    """
    parsed_json = json.loads(json_string)
    flattened_json = json.dumps(parsed_json, separators=(",", ":"))
    return flattened_json
