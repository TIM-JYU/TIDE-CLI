from dataclasses import dataclass
from pathlib import Path, PurePath
from typing import List

import pytest
from click.testing import CliRunner
from conftest import tmp_dir_path

from tidecli.main import task

# TASK LIST


def test_task_list():
    pass


def test_task_list_json():
    pass


# TASK CREATE


def test_create_task_with_supplementary_files_defined_in_csplugin(tmp_dir):
    pass


def test_create_task_with_supplementary_files_from_external_source(tmp_dir):
    pass


def test_create_task_with_supplementary_files_from_tim_source(tmp_dir):
    pass


@dataclass
class ExpectedTaskFile:
    expected_filename: str
    expected_content: str | None = (
        None  # None is used to ignore the content during tests
    )


@pytest.mark.parametrize(
    "course_path, exercise_id, task_id, expected_files",
    [
        # task with no supplementary files
        (
            "users/test-user-1/course-2",
            "exercise-a",
            "t2",
            [
                ExpectedTaskFile(
                    expected_filename="hello.py",
                    expected_content='print("marsu maiskuttaa")',
                )
            ],
        )
        # task with supplementary files defined in markdown
        # task with supplementary files from TIM source
        # task with supplementary files from external source
    ],
)
def test_create_task_single_creates_task_files_with_expected_content(tmp_dir, course_path: str, exercise_id: str, task_id: str, expected_files: List[ExpectedTaskFile]):
    """Check that creating a single task creates the expected task files with expected content in the expected location"""
    runner = CliRunner()

    runner.invoke(
        task,
        [
            "create",
            str(PurePath(course_path, exercise_id)),
            task_id,
            "-d",
            tmp_dir_path,
        ],
    )

    for expected_file in expected_files:
        task_file_path = Path(tmp_dir_path, exercise_id, task_id, expected_file.expected_filename)

        try:
            file = open(task_file_path)
        except FileNotFoundError:
            pytest.fail(
                f'Expected file "{expected_file.expected_filename}" not found in temporary directory.'
            )
        else:
            if expected_file.expected_content is not None:
                with file:
                    content = file.read()
                    assert content == expected_file.expected_content


def test_create_task_single_creates_timdata_file(tmp_dir):
    exercise_id = "exercise-a"
    task_id = "t2"
    timdata_file_name = ".timdata"
    timdata_file_path = Path(tmp_dir_path, exercise_id, task_id, timdata_file_name)
    runner = CliRunner()

    runner.invoke(
        task,
        [
            "create",
            f"users/test-user-1/course-2/{exercise_id}",
            task_id,
            "-d",
            tmp_dir_path,
        ],
    )

    assert timdata_file_path.is_file()


def test_create_task_with_force_flag(tmp_dir):
    pass


def test_create_all_tasks_for_exercise(tmp_dir):
    # TODO: test that creating tasks with --all flag works
    pass


# TASK SUBMIT


def test_task_submit():
    """Submit an answer to a course."""
    pass


def test_task_submit_invalid_path():
    """Submit an answer to a course."""
    pass


def test_task_submit_invalid_answer_file():
    """Submit an answer to a course."""
    pass


def test_task_submit_invalid_meta_data():
    """Submit an answer to a course."""
    pass


# TASK RESET


def test_task_reset(tmp_dir):
    pass
