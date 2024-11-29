from pathlib import Path
from click.testing import CliRunner
from constants import TEMPORARY_DIRECTORY
from tidecli.main import task
from utils import temporary_directory_file_contents_match_expected, copy_directory_from_expected_to_temporary


def test_create_single_task_with_force_flag(tmp_dir):
    """
    Test that the task files are overwritten when the force flag is used.

    param: tmp_dir: Temporary directory for the test as a fixture.
    """

    # Define variables for paths and file name
    course_path = "users/test-user-1/course-1/"
    exercise_id = "exercise-1"
    task_id = "t1"
    task_file = "hello.cs"
    exercise_path = str(Path(course_path, exercise_id))
    local_path = Path(TEMPORARY_DIRECTORY, exercise_id, task_id)

    # Copy the expected task files to the local path
    copy_directory_from_expected_to_temporary(exercise_id, task_id)

    # Modify the file
    hello = open(Path(local_path, task_file), "w")
    hello.write("foofoo")
    hello.close()

    # Run the command to overfrite the task files
    runner = CliRunner()
    runner.invoke(
        task,
        [
            "create",
            exercise_path,
            task_id,
            "-f",
            "-d",
            TEMPORARY_DIRECTORY,
        ],
    )

    # TODO: CLI could be improved to return other return codes also than just 0.
    # TODO: Because if returncode will be other than 0, then the test will fail.

    # Check that the file has been overwritten
    mismatches = temporary_directory_file_contents_match_expected(exercise_id, task_id)
    assert len(mismatches) == 0
