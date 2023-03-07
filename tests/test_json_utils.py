import core.json_utils as ju


def test_format_json() -> None:
    json_actual = """{"wKey":100,"zKey":true,"aKey":{"newObj":["key1","aKey"]}}"""
    json_expected = """{
    "wKey": 100,
    "zKey": true,
    "aKey": {
        "newObj": [
            "key1",
            "aKey"
        ]
    }
}"""
    result = ju.format_json(json_actual, sort_keys=False)
    assert result == json_expected


def test_format_json_with_params() -> None:
    json_actual = """{"wKey":100,"zKey":true,"aKey":{"newObj":["key1","aKey"]}}"""
    json_expected = """{
  "aKey": {
    "newObj": [
      "key1",
      "aKey"
    ]
  },
  "wKey": 100,
  "zKey": true
}"""
    result = ju.format_json(json_actual, indentation=2, sort_keys=True)
    assert result == json_expected


def test_validate_json() -> None:
    json_actual_valid = """{"wKey":100,"zKey":true,"aKey":{"newObj":["key1","aKey"]}}"""
    json_actual_invalid = """{"wKey":100,"zKey:true,"aKey":"newObj":["key1","aKey"]}}"""

    assert ju.validate_json(json_actual_valid) == ""
    assert len(ju.validate_json(json_actual_invalid)) > 0


def test_flatten_json() -> None:
    json_actual = """{
  "aKey": {
    "newObj": [
      "key1",
      "aKey"
    ]
  },
  "wKey": 100,
  "zKey": true
}"""
    json_expected = """{"aKey":{"newObj":["key1","aKey"]},"wKey":100,"zKey":true}"""
    result = ju.flatten_json(json_actual)

    assert result == json_expected
