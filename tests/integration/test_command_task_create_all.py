from pathlib import Path
from click.testing import CliRunner
from constants import TEMPORARY_DIRECTORY
from tidecli.main import task
from utils import get_file_structure_differences_in_temporary_and_expected_directories


def test_create_all_tasks_for_exercise(tmp_dir):

    exercise_id = "exercise-a"
    tasks = [
        "t1",
        "t2",
        "t4",
    ]

    runner = CliRunner()
    runner.invoke(
        task,
        [
            "create",
            str(Path("users/test-user-1/course-2", exercise_id)),
            "-a",
            "-d",
            TEMPORARY_DIRECTORY,
        ],
    )

    for task_id in tasks:
        structure_differences = (
            get_file_structure_differences_in_temporary_and_expected_directories(
                exercise_id, task_id
            )
        )
        assert (
            structure_differences.get_mismatch_count() == 0
        ), f"Found differences: {structure_differences}"
