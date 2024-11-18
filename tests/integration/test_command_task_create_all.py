
from dataclasses import dataclass
from pathlib import Path
from typing import List

import pytest
from click.testing import CliRunner
from conftest import tmp_dir_path

from utils import validate_json
from tidecli.main import task


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

