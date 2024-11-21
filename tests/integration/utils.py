import json


def is_valid_json(data: str) -> bool:
    try:
        json.loads(data)
    except json.JSONDecodeError:
        return False
    return True


def temporary_directory_file_structure_matches_expected(exercise_id: str, task_id: str | None) -> bool:
    pass


def temporary_directory_file_contents_match_expected(exercise_id: str, task_id: str | None) -> bool:
    pass
