"""Run integration tests either locally or in CI."""

import json
import pytest
from click.testing import CliRunner
from tidecli.main import courses


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
