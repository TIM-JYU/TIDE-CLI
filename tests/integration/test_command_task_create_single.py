from pathlib import Path
from typing import List

import pytest
from click.testing import CliRunner

from utils import (
    temporary_directory_file_contents_match_expected,
    get_file_structure_differences_in_temporary_and_expected_directories,
)
from tidecli.main import task
from constants import TEMPORARY_DIRECTORY


def test_task_create_single_creates_all_expected_files(tmp_dir):
    exercise_id = "exercise-a"
    task_id = "t2"

    runner = CliRunner()
    runner.invoke(
        task,
        [
            "create",
            str(Path("users/test-user-1/course-2", exercise_id)),
            task_id,
            "-d",
            TEMPORARY_DIRECTORY,
        ],
    )

    structure_differences = (
        get_file_structure_differences_in_temporary_and_expected_directories(
            exercise_id, task_id
        )
    )

    assert (
        structure_differences.get_mismatch_count() == 0
    ), f"File structures do not match. {str(structure_differences)}"


def test_task_create_single_creates_files_with_expected_content(tmp_dir):
    exercise_id = "exercise-a"
    task_id = "t2"

    runner = CliRunner()
    runner.invoke(
        task,
        [
            "create",
            str(Path("users/test-user-1/course-2", exercise_id)),
            task_id,
            "-d",
            TEMPORARY_DIRECTORY,
        ],
    )

    mismatches = temporary_directory_file_contents_match_expected(exercise_id, task_id)

    assert (
        len(mismatches) == 0
    ), f"Found mismatching content in the following files: {', '.join(mismatches)}"
