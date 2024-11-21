import filecmp
import json
from pathlib import Path

from tests.integration.constants import EXPECTED_TASK_FILES_DIRECTORY, TEMPORARY_DIRECTORY


def is_valid_json(data: str) -> bool:
    try:
        json.loads(data)
    except json.JSONDecodeError:
        return False
    return True


def temporary_directory_file_structure_matches_expected(exercise_id: str, task_id: str | None) -> bool:
    """
    Returns true if the file structure of temporary and expected directories match.
    """
    # TODO: info about differences: unexpected file found / expected file not found
    def get_structure(directory: Path):
        base_path = directory.resolve()
        return {path.relative_to(base_path) for path in base_path.rglob('*')}

    temporary_structure = get_structure(Path(TEMPORARY_DIRECTORY, exercise_id, task_id if task_id else ''))
    expected_structure = get_structure(Path(EXPECTED_TASK_FILES_DIRECTORY, exercise_id, task_id if task_id else ''))
    
    return temporary_structure == expected_structure


def temporary_directory_file_contents_match_expected(exercise_id: str, task_id: str | None) -> bool:
    """
    Returns true if contents of all files COMMON to temporary and expected directories match.

    Does not care about files present only in one temporary or expected directory.
    """
    temporary_files_path = Path(TEMPORARY_DIRECTORY, exercise_id, task_id if task_id else '').resolve()
    expected_files_path = Path(EXPECTED_TASK_FILES_DIRECTORY, exercise_id, task_id if task_id else '').resolve()

    def dir_files_contents_match(dir1: Path, dir2: Path) -> bool:
        dir_cmp = filecmp.dircmp(dir1, dir2)
        match, mismatch, errors = filecmp.cmpfiles(
            dir_cmp.left, dir_cmp.right, dir_cmp.common_files, shallow=False
        )

        if mismatch or errors:
            return False

        # Compare subdirectories recursively
        for sub_dir in dir_cmp.subdirs.values():
            if not dir_files_contents_match(
                Path(sub_dir.left),
                Path(sub_dir.right),
            ):
                return False

        return True

    return dir_files_contents_match(temporary_files_path, expected_files_path)

