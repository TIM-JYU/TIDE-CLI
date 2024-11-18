from dataclasses import dataclass
from pathlib import Path
from typing import List

import pytest
from click.testing import CliRunner
from conftest import tmp_dir_path

from utils import validate_json
from tidecli.main import task

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
