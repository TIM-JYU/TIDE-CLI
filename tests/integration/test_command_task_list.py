
from dataclasses import dataclass
from pathlib import Path
from typing import List

import pytest
from click.testing import CliRunner
from conftest import tmp_dir_path

from utils import validate_json
from tidecli.main import task

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

    # TODO: is_valid_json ja assert tassa
    validate_json(result.output)


def test_task_list_with_json_flag_outputs_expected_data():
    # TODO: the current "task list --json" prints tons of unnecessary information
    pass
