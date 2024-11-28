from pathlib import Path

import pytest
from click.testing import CliRunner

from utils import copy_directory_from_expected_to_temporary 
from tidecli.main import task
from constants import TEMPORARY_DIRECTORY

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
    task_file_path = Path(TEMPORARY_DIRECTORY, exercise_id, task_id, "hello.cs")

    copy_directory_from_expected_to_temporary(exercise_id, task_id)

    # edit the file to be reset
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
