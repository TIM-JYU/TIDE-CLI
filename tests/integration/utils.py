import json

import pytest


def validate_json(data: str):
    try:
        json.loads(data)
    except json.JSONDecodeError:
        pytest.fail("Output is not valid JSON")
