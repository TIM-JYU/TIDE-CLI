from dataclasses import dataclass
from pathlib import Path
from typing import List

import pytest
from click.testing import CliRunner
from conftest import tmp_dir_path

from utils import validate_json
from tidecli.main import task


@dataclass
class ExpectedTaskFile:
    filename: str
    content: str | None = None  # None is used to ignore the content during tests


task_exercises_params = [
    ("exercise-1", "users/test-user-1/course-1/exercise-1", ["t1", "t2", "t3"]),
    ("exercise-2", "users/test-user-1/course-1/exercise-2", ["33232123"]),
    ("exercise-a", "users/test-user-1/course-2/exercise-a", ["t1", "t2", "t4"]),
    ("exercise-b", "users/test-user-1/course-2/exercise-b", ["t1"]),
]

# TODO: content attributes may have to be match actual content
task_content_params = [
    # task with no supplementary files
    (
        "users/test-user-1/course-2",
        "exercise-a",
        "t2",
        [
            ExpectedTaskFile(
                filename="hello.py",
                content='print("marsu maiskuttaa")',
            ),
            ExpectedTaskFile(filename=".timdata"),
        ],
    ),
    # task with supplementary files defined in markdown
    (
        "users/test-user-1/course-1",
        "exercise-1",
        "t2",
        [
            ExpectedTaskFile(
                filename="animals.py"
                # TODO: how to handle file content with BYCODE tags
            ),
            ExpectedTaskFile(
                filename="kissa.txt",
                content="istuu\nja\nnaukuu\n",
            ),
            ExpectedTaskFile(filename="koira.dat", content="seisoo ja haukkuu"),
            ExpectedTaskFile(filename=".timdata"),
        ],
    ),
    # task with supplementary files autogenerated by TIM
    (
        "users/test-user-1/course-1",
        "exercise-1",
        "t3",
        [
            ExpectedTaskFile(filename="hello.cs"),
            ExpectedTaskFile(filename="t3.csproj"),
            ExpectedTaskFile(filename=".timdata"),
        ],
    ),
    # task with supplementary files from external source
    (
        "users/test-user-1/course-2",
        "exercise-b",
        "t1",
        [
            ExpectedTaskFile(filename="hevonen.py",
                             content='print("hevonen juo limsaa")\n'),
            ExpectedTaskFile(filename="logo.svg"),
            ExpectedTaskFile(filename=".timdata"),
        ],
    ),
    # TODO: task with supplementary files from TIM source
]


# TASK LIST


@pytest.mark.parametrize("exercise, exercise_path, expected_task_ids", task_exercises_params)
def test_task_list_outputs_expected_data(exercise: str,
                                         exercise_path: str,
                                         expected_task_ids: List[str]):
    runner = CliRunner()
    result = runner.invoke(
        task,
        ["list", exercise_path],
    )

    assert all([task_id in result.output for task_id in expected_task_ids])


def test_task_list_with_json_flag_outputs_valid_json():
    runner = CliRunner()
    result = runner.invoke(
        task,
        ["list", "users/test-user-1/course-1/exercise-1", "--json"],
    )

    validate_json(result.output)


def test_task_list_with_json_flag_outputs_expected_data():
    # TODO: the current "task list --json" prints tons of unnecessary information
    pass


# TASK CREATE


@pytest.mark.parametrize("course_path, exercise_id, task_id, expected_files", task_content_params)
def test_create_single_task_creates_files_with_expected_content(
    course_path: str,
    exercise_id: str,
    task_id: str,
    expected_files: List[ExpectedTaskFile],
    tmp_dir,
):
    """Check that creating a single task creates the expected task files with expected content in the expected location"""
    runner = CliRunner()

    runner.invoke(
        task,
        [
            "create",
            str(Path(course_path, exercise_id)),
            task_id,
            "-d",
            tmp_dir_path,
        ],
    )

    for expected_file in expected_files:
        task_file_path = Path(
            tmp_dir_path, exercise_id, task_id, expected_file.filename
        )

        try:
            file = open(task_file_path)
        except FileNotFoundError:
            pytest.fail(
                f'Expected file "{
                    expected_file.filename}" not found in temporary directory.'
            )
        else:
            if expected_file.content is not None:
                with file:
                    content = file.read()
                    assert content == expected_file.content


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
            str(Path("users/test-user-1/course-2", exercise_id)),
            task_id,
            "-d",
            tmp_dir_path,
        ],
    )

    assert timdata_file_path.is_file()


@pytest.mark.parametrize("course_path, exercise_id, task_id, expected_files", task_content_params)
def test_create_task_with_force_flag(exercise_id: str, course_path: str, task_id: str, expected_files: list, tmp_dir):
    current_exercise = str(Path(course_path, exercise_id))
    local_path = Path(tmp_dir_path, exercise_id, task_id)
    runner = CliRunner()
    runner.invoke(
        task,
        [
            "create",
            current_exercise,
            task_id,
            "-d",
            tmp_dir_path,
        ],
    )

    for expected_file in expected_files:
        with open(Path(local_path, expected_file.filename), "w") as task_file:
            task_file.write("foofoo")
            task_file.close()

    run = runner.invoke(
        task,
        [
            "create",
            current_exercise,
            task_id,
            "-f",
            "-d",
            tmp_dir_path,
        ],
    )

    for expected_file in expected_files:
        task_file = open(Path(local_path, expected_file.filename), "r")
        content = task_file.read()
        task_file.close()

        # TODO: improve content asserts, now just check the content change
        assert content != "foofoo"

    # TODO: CLI could be improved to return other return codes also than just 0.
    assert run.exit_code == 0


@pytest.mark.parametrize("exercise, exercise_path, expected_task_ids", task_exercises_params)
def test_create_all_tasks_for_exercise(exercise: str, exercise_path: str, expected_task_ids: list[str], tmp_dir):
    runner = CliRunner()

    runner.invoke(
        task,
        [
            "create",
            str(Path(exercise_path)),
            "-a",
            "-d",
            tmp_dir_path,
        ],
    )

    for task_id in expected_task_ids:
        assert Path(tmp_dir_path, exercise, task_id).is_dir()
        assert Path(tmp_dir_path, exercise, task_id, ".timdata").is_file()


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


@pytest.mark.parametrize(
    "replace_line_idx, expected_to_exist_after_reset, error_msg",
    [
        # TODO: change the fail messages to not use "bycode"
        (0, False, "Changes before bycode tag were not reset"),
        (-1, False, "Changes after bycode tag were not reset"),
        (5, True, "Changes between bycode tags were reset"),
    ],
)
def test_task_reset(
    tmp_dir, replace_line_idx: int, expected_to_exist_after_reset: bool, error_msg: str
):
    exercise_id = "exercise-1"
    task_id = "t3"
    inserted_str = "ThIsLiNeWaSeDiTeDwHiLeTeStInG"

    runner = CliRunner()

    runner.invoke(
        task,
        [
            "create",
            str(Path("users/test-user-1/course-1", exercise_id)),
            task_id,
            "-d",
            tmp_dir_path,
        ],
    )

    task_file_path = Path(tmp_dir_path, exercise_id, task_id, "hello.cs")

    with open(task_file_path, "r+") as f:
        file_content = f.readlines()
        file_content[replace_line_idx] = inserted_str

        f.seek(0)
        f.write("\n".join(file_content))
        f.truncate()

    runner.invoke(
        task,
        [
            "reset",
            str(task_file_path),
        ],
    )

    with open(task_file_path, "r") as f:
        reset_file_content = f.read()

    assert (
        inserted_str in reset_file_content
    ) == expected_to_exist_after_reset, error_msg
