import json

import pytest


# TODO: make this return bool and rename
def validate_json(data: str):
    try:
        json.loads(data)
    except json.JSONDecodeError:
        pytest.fail("Output is not valid JSON")

def directory_file_names_match_expected(exercise_id: str, task_id: str | None, temp_dir: str) -> bool:
    pass


def directory_file_contents_match_expected(exercise_id: str, task_id: str | None, temp_dir: str) -> bool:
    pass
    
