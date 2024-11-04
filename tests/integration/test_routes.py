"""Run integration tests either locally or in CI."""

import os
import tim_api

USERNAME = os.environ.get("TIM_USERNAME", "testuser1")

def test_get_profile():
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
