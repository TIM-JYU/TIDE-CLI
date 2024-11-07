"""Run integration tests either locally or in CI."""

import json
from typing import List
import pytest
from click.testing import CliRunner
from tidecli.main import courses


@pytest.mark.parametrize(
        'extra_flags', [
            ([]),
            (['--json'])
            ]
        )
def test_get_courses_outputs_expected_data(extra_flags: List[str]):
    """
    Check that output includes names of all the courses and task documents.
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

    result = runner.invoke(courses, extra_flags)
    assert all([substr in result.output for substr in expected_substrings]), f"Output is missing course and/or task names when run with flags {extra_flags}."


# def test_get_courses_with_json_flag_outputs_expected_data():
#     runner = CliRunner()
#     expected_substrings = [
#         "course-1-landing-page",
#         "exercise-1",
#         "exercise-2",
#         "course-2-landing-page",
#         "exercise-a",
#         "exercise-b",
#     ]

#     result = runner.invoke(courses, ["--json"])

#     assert all([substr in result.output for substr in expected_substrings])


def test_get_courses_with_json_flag_outputs_valid_json():
    """
    Check that all the task documents and courses are returned, and that the output is valid JSON.
    """
    runner = CliRunner()

    result = runner.invoke(courses, ["--json"])

    try:
        json.loads(result.output)
    except json.JSONDecodeError:
        pytest.fail("Output is not valid JSON")
