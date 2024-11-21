from pathlib import Path
import pytest
from click.testing import CliRunner
from constants import TEMPORARY_DIRECTORY
from tidecli.main import task

task_exercises_params = [
    (
        "ex",
        "ex_path",
        []
    )
]


@pytest.mark.parametrize("exercise, exercise_path, expected_task_ids",
                         task_exercises_params)
def test_create_all_tasks_for_exercise(exercise: str,
                                       exercise_path: str,
                                       expected_task_ids: list[str],
                                       tmp_dir):

    runner = CliRunner()
    runner.invoke(
        task,
        [
            "create",
            str(Path(exercise_path)),
            "-a",
            "-d",
            TEMPORARY_DIRECTORY,
        ],
    )

    for task_id in expected_task_ids:
        assert Path(TEMPORARY_DIRECTORY, exercise, task_id).is_dir()
        assert Path(TEMPORARY_DIRECTORY, exercise, task_id, ".timdata").is_file()

    assert False
