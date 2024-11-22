from pathlib import Path
from typing import List

import pytest
from click.testing import CliRunner

from utils import temporary_directory_file_contents_match_expected, temporary_directory_file_structure_matches_expected
from tidecli.main import task
from constants import TEMPORARY_DIRECTORY


def test_task_create_single_creates_expected_files(tmp_dir):
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
     
    assert temporary_directory_file_structure_matches_expected(exercise_id, task_id)
    


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

    assert len(mismatches) == 0, f"Found mismatching content in the following files: {', '.join(mismatches)}"

