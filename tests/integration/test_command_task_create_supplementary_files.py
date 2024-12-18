# TODO: repair the functions in this file. They have not been updated to use the updated file content and structure functions in asserts
from pathlib import Path

import pytest
from click.testing import CliRunner

from tidecli.main import task
from constants import TEMPORARY_DIRECTORY
from utils import (
    temporary_directory_file_contents_mismatches,
    get_file_structure_differences_in_temporary_and_expected_directories,
)

tasks_with_supplementary_files_headers = (
    "course_path, exercise_id, task_id, supplementary_file_description"
)

tasks_with_supplementary_files = [
    # (course, exercise, task, supplementary file description)
    ("users/test-user-1/course-1", "exercise-1", "t2", "defined in markdown"),
    ("users/test-user-1/course-1", "exercise-1", "t3", "fetched from external source"),
    ("users/test-user-1/course-2", "exercise-b", "t1", "fetched from TIM"),
]


@pytest.mark.parametrize(
    tasks_with_supplementary_files_headers, tasks_with_supplementary_files
)
def test_task_create_with_supplementary_files_creates_expected_files(
    course_path, exercise_id, task_id, supplementary_file_description, tmp_dir
):
    runner = CliRunner()
    runner.invoke(
        task,
        [
            "create",
            str(Path(course_path, exercise_id)),
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
    ), f"File structures do not match when creating task with supplementary files {supplementary_file_description}. {str(structure_differences)}"


@pytest.mark.parametrize(
    tasks_with_supplementary_files_headers, tasks_with_supplementary_files
)
def test_task_create_with_supplementary_files_creates_files_with_expected_content(
    course_path, exercise_id, task_id, supplementary_file_description, tmp_dir
):
    runner = CliRunner()
    runner.invoke(
        task,
        [
            "create",
            str(Path(course_path, exercise_id)),
            task_id,
            "-d",
            TEMPORARY_DIRECTORY,
        ],
    )

    mismatches = temporary_directory_file_contents_mismatches(exercise_id, task_id)
    assert (
        len(mismatches) == 0
    ), f"Unexpected file content when creating task with supplementary files {supplementary_file_description}"
