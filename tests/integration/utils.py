from dataclasses import dataclass
import filecmp
import json
from pathlib import Path
from typing import List, Tuple

from constants import EXPECTED_TASK_FILES_DIRECTORY, TEMPORARY_DIRECTORY


def is_valid_json(data: str) -> bool:
    try:
        json.loads(data)
    except json.JSONDecodeError:
        return False
    return True

@dataclass
class StructureDifferences:
    missing_files: List[str]
    unexpected_files: List[str]

    def __str__(self):
        string = ""
        if self.missing_files:
            string += (f"Missing files/directories: {', '.join(self.missing_files)}.")
        else:
            string += "No missing files/directories."

        if self.unexpected_files:
            string += (f"Unexpected files: {', '.join(self.unexpected_files)}.")
        else:
            string += "No unexpected files/directories."

        return string

    def get_mismatch_count(self):
        return len(self.missing_files) + len(self.unexpected_files)


def get_file_structure_differences_in_temporary_and_expected_directories(exercise_id: str, task_id: str | None) -> StructureDifferences:
    """
    Returns true if the file structure of temporary and expected directories match.
    """
    def get_structure(directory: Path):
        base_path = directory.resolve()
        return {path.relative_to(base_path) for path in base_path.rglob('*')}

    temporary_structure = get_structure(Path(TEMPORARY_DIRECTORY, exercise_id, task_id if task_id else ''))
    expected_structure = get_structure(Path(EXPECTED_TASK_FILES_DIRECTORY, exercise_id, task_id if task_id else ''))

    missing_files = expected_structure - temporary_structure
    unexpected_files = temporary_structure - expected_structure
    
    return StructureDifferences(
            missing_files=list(str(p) for p in missing_files), 
            unexpected_files=list(str(p) for p in unexpected_files))


# TODO: report file names (and lines) that mismatch
def temporary_directory_file_contents_match_expected(exercise_id: str, task_id: str | None) -> List[str]:
    """
    Returns true if contents of all files COMMON to temporary and expected directories match.

    Does not care about files present only in one temporary or expected directory.
    """
    temporary_files_path = Path(TEMPORARY_DIRECTORY, exercise_id, task_id if task_id else '').resolve()
    expected_files_path = Path(EXPECTED_TASK_FILES_DIRECTORY, exercise_id, task_id if task_id else '').resolve()
    caught_mismatches: List[str] = []

    def dir_files_contents_match(dir1: Path, dir2: Path):
        dir_cmp = filecmp.dircmp(dir1, dir2)
        match, mismatch, errors = filecmp.cmpfiles(
            dir_cmp.left, dir_cmp.right, dir_cmp.common_files, shallow=False
        )

        caught_mismatches.extend(mismatch)

        # Compare subdirectories recursively
        for sub_dir in dir_cmp.subdirs.values():
            dir_files_contents_match(
                Path(sub_dir.left),
                Path(sub_dir.right),
                )

    dir_files_contents_match(temporary_files_path, expected_files_path)

    return caught_mismatches

