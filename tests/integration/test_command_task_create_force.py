from dataclasses import dataclass
from pathlib import Path
from typing import List

import pytest
from click.testing import CliRunner
from conftest import tmp_dir_path

from utils import validate_json
from tidecli.main import task

# TODO: yksinkertaista, tässä riittää testata esim. vain yksi tiedosto
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

    # TODO: Kommentoi
    for expected_file in expected_files:
        task_file = open(Path(local_path, expected_file.filename), "r")
        content = task_file.read()
        task_file.close()

        # TODO: improve content asserts, now just check the content change
        assert content != "foofoo"

    # TODO:  CLI could be improved to return other return codes also than just 0.
    assert run.exit_code == 0




