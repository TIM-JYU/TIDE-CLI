from typing import List

import pytest
from click.testing import CliRunner

from utils import is_valid_json
from tidecli.main import task
from tidecli.main import task

task_exercises_params = [
    ("exercise-1", "users/test-user-1/course-1/exercise-1", ["t1", "t2", "t3"]),
    ("exercise-2", "users/test-user-1/course-1/exercise-2", ["33232123"]),
    ("exercise-a", "users/test-user-1/course-2/exercise-a", ["t1", "t2", "t4"]),
    ("exercise-b", "users/test-user-1/course-2/exercise-b", ["t1"]),
]

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
    assert is_valid_json(result.output), "Output is not valid JSON."


def test_task_list_with_json_flag_outputs_expected_data():
    # TODO: the current "task list --json" prints tons of unnecessary information
    pass
