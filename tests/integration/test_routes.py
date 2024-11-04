"""Run integration tests either locally or in CI."""

import os

from selenium.webdriver.common.by import By
import pytest
import webbrowser
from selenium import webdriver
from click.testing import CliRunner

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

    # assert isinstance(res, list)
    pass

def test_submit_answer():
    """Submit an answer to a course."""
    # TODO: Write small codefile and submit it
    pass


def mock_browser_open(url: str):
    # logger = logging.getLogger('selenium')
    # logger.setLevel(logging.DEBUG)
    # logger.debug("hello from selenium")
    # driver = webdriver.Firefox()
    # driver.get(url)
    # driver.implicitly_wait(2)
    # login_form = driver.find_element(By.CLASS_NAME, "logolink")
    # login_form.click()
    print(f"url: {url}")
    return 


def test_login(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr("webbrowser.open", mock_browser_open)
    import tidecli.main as app
    runner = CliRunner()
    result = runner.invoke(app.login)
    assert result == -1
