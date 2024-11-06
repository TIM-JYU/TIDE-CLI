"""Run integration tests either locally or in CI."""

import os

from selenium.webdriver.common.by import By
import pytest
import webbrowser
from selenium import webdriver
from click.testing import CliRunner

from tidecli.main import courses

USERNAME = os.environ.get("TIM_USERNAME", "testuser1")

def test_get_profile():
    import tim_api
    """Get user profile, check username correctness."""
    res = tim_api.get_current_user()
    assert res.user_name == USERNAME


def test_get_courses():
    """
    Get all IDE compatible courses.

    Courses has to be set to My courses bookmarks.
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
    expected_substrings = ["course-1-landing-page", "exercise-1", "exercise-2", "course-2-landing-page", "exercise-a", "exercise-b"]

    result = runner.invoke(courses)
    assert all([substr in result.output for substr in expected_substrings])


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
