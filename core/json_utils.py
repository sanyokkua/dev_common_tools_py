import json


def format_json(json_string: str, indentation: int = 4, sort_keys: bool = True) -> str:
    parsed_json = json.loads(json_string)
    formatted_json = json.dumps(parsed_json, indent=indentation, sort_keys=sort_keys)
    return formatted_json


def validate_json(json_string: str) -> str:
    try:
        json.loads(json_string)
    except json.JSONDecodeError as e:
        return e.__str__()
    return ""


def flatten_json(json_string: str) -> str:
    parsed_json = json.loads(json_string)
    flattened_json = json.dumps(parsed_json, separators=(",", ":"))
    return flattened_json
