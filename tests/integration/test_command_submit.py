from pathlib import Path

import pytest
from click.testing import CliRunner

from tidecli.main import submit
from constants import TEMPORARY_DIRECTORY
from utils import copy_directory_from_expected_to_temporary


def test_task_submit(tmp_dir):
    """Submit an answer to a task."""
    answer_str = "#the horse drinks heineken" 

    exercise_id = "exercise-b"
    task_id = "t1"
    copy_directory_from_expected_to_temporary(exercise_id)

    # edit the file to be submitted
    with open(Path(TEMPORARY_DIRECTORY, exercise_id, task_id, "hevonen.py"), "r+") as f:
        file_content = f.readlines()
        file_content[0] = answer_str

        f.seek(0)
        f.write("\n".join(file_content))
        f.truncate()

    runner = CliRunner()
    res = runner.invoke(
        submit,
        [
            str(Path(TEMPORARY_DIRECTORY, exercise_id, task_id)),
        ],
    )

    assert res.exit_code == 0
    # TODO: currently the answer is not saved because conftest has no teardown for the test documents residing in TIM, thus this test tries to submit the same answer again. This results in "not saved..." response.
    # assert "Saved new answer successfully." in res.output


@pytest.mark.xfail
def test_task_submit_invalid_path():
    pass
    pytest.xfail()


@pytest.mark.xfail
def test_task_submit_invalid_answer_file():
    pass
    pytest.xfail()


@pytest.mark.xfail
def test_task_submit_invalid_meta_data():
    pass
    pytest.xfail()
