from pathlib import Path

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


def test_create_task_single(tmp_dir):
    """Check that creating a single task creates the expected task files with expected content in the expected location"""
    runner = CliRunner()
    exercise_id = "exercise-a"
    task_id = "t2"

    result = runner.invoke(
        task,
        [
            "create",
            f"users/test-user-1/course-2/{exercise_id}",
            task_id,
            "-d",
            tmp_dir_path,
        ],
    )
    print(result.output)

    task_file_name = "hello.py"
    task_file_path = Path(tmp_dir_path, exercise_id, task_id, task_file_name)
    try:
        file = open(task_file_path)
    except FileNotFoundError:
        pytest.fail(
            f'Expected file "{task_file_name}" not found in temporary directory.'
        )
    else:
        with file:
            content = file.read()
            assert content == 'print("marsu maiskuttaa")'

    timdata_file_name = ".timdata"
    timdata_file_path = Path(tmp_dir_path, exercise_id, task_id, timdata_file_name)
    assert timdata_file_path.is_file()


def test_create_task_with_supplementary_files(tmp_dir):
    # TODO: task with supplementary files
    pass


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
