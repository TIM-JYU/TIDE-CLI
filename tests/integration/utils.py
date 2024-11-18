import json

import pytest


def is_valid_json(data: str) -> bool:
    try:
        json.loads(data)
    except json.JSONDecodeError:
        return False
    return True

def directory_file_names_match_expected(exercise_id: str, task_id: str | None, temp_dir: str) -> bool:
    pass


def directory_file_contents_match_expected(exercise_id: str, task_id: str | None, temp_dir: str) -> bool:
    return False
    
