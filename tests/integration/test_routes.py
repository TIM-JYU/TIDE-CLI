"""Run integration tests either locally or in CI."""

import json
import os
from pathlib import Path

import pytest
from click.testing import CliRunner
from conftest import tmp_dir_path

from tidecli.main import courses, task

USERNAME = os.environ.get("TIM_USERNAME", "testuser1")


def test_get_profile():
    import tim_api

    """Get user profile, check username correctness."""
    res = tim_api.get_current_user()
    assert res.user_name == USERNAME


def test_get_courses():
    """
    Check that all the task documents and courses are returned, and that the output is valid JSON.
    """
    # TODO: Implement fetching test, handle the keyring credentials
    # TODO: Keyring might be possible to bypass on testing

    # Example of expected output of the command, IDs will vary
    # Course: users/test-user-1/course-2/course-2-landing-page, ID: 95
    # - exercise-a, ID: 93, Path: users/test-user-1/course-2/exercise-a
    # - exercise-b, ID: 94, Path: users/test-user-1/course-2/exercise-b

    # Course: users/test-user-1/course-1/course-1-landing-page, ID: 91
    # - exercise-1, ID: 89, Path: users/test-user-1/course-1/exercise-1
    # - exercise-2, ID: 90, Path: users/test-user-1/course-1/exercise-2

    runner = CliRunner()
    expected_substrings = [
        "course-1-landing-page",
        "exercise-1",
        "exercise-2",
        "course-2-landing-page",
        "exercise-a",
        "exercise-b",
    ]

    result = runner.invoke(courses)
    assert all([substr in result.output for substr in expected_substrings])


def test_get_courses_json():
    """
    Check that all the task documents and courses are returned, and that the output is valid JSON.
    """
    runner = CliRunner()
    expected_substrings = [
        "course-1-landing-page",
        "exercise-1",
        "exercise-2",
        "course-2-landing-page",
        "exercise-a",
        "exercise-b",
    ]

    result = runner.invoke(courses, ["--json"])

    try:
        json.loads(result.output)
    except json.JSONDecodeError:
        pytest.fail("Output is not valid JSON")

    assert all([substr in result.output for substr in expected_substrings])


def test_create_single_task(tmp_dir):
    """Check that creating a single task creates the expected task file with expected content in the expected location"""
    runner = CliRunner()
    exercise_id = "exercise-a"
    task_id = "t2"

    result = runner.invoke(task, ["create", f"users/test-user-1/course-2/{exercise_id}", task_id, "-d", tmp_dir_path])
    print(result.output)

    task_file_name = "hello.py"
    task_file_path = Path(tmp_dir_path, exercise_id, task_id, task_file_name) 
    try:
        file = open(task_file_path)
    except FileNotFoundError:
        pytest.fail(f"Expected file \"{task_file_name}\" not found in temporary directory.")
    else:
        with file:
            content = file.read()
            assert content == "print(\"marsu maiskuttaa\")"



def test_submit_answer():
    """Submit an answer to a course."""
    # TODO: Write small codefile and submit it
    pass


# def mock_browser_open(url: str):
# logger = logging.getLogger('selenium')
# logger.setLevel(logging.DEBUG)
# logger.debug("hello from selenium")
# driver = webdriver.Firefox()
# driver.get(url)
# driver.implicitly_wait(2)
# login_form = driver.find_element(By.CLASS_NAME, "logolink")
# login_form.click()
# print(f"url: {url}")
# return


# def test_login(monkeypatch: pytest.MonkeyPatch):
# monkeypatch.setattr("webbrowser.open", mock_browser_open)
# import tidecli.main as app
# runner = CliRunner()
# result = runner.invoke(app.login)
# assert result == -1
