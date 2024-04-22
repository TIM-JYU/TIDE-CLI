import unittest
from unittest.mock import patch, MagicMock

import click

from tests.test_data import (
    validate_token_response,
    get_profile_test_response,
    get_ide_courses_test_response,
    get_tasks_by_doc_test_response,
    get_task_by_ide_task_id_test_response,
    submit_task_by_id_test_response,
    submit_task_by_id_tim_test_response,
)
from tidecli.api.routes import (
    validate_token,
    get_profile,
    get_ide_courses,
    get_tasks_by_doc,
    get_task_by_ide_task_id,
    submit_task,
)
from tidecli.models.course import Course
from tidecli.models.submit_data import SubmitData
from tidecli.models.task_data import TaskData
from tidecli.models.tim_feedback import TimFeedback


class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.mock_response = MagicMock()
        self.patch = patch(
            "tidecli.api.routes.requests.request", return_value=self.mock_response
        )

    def test_validate_token(self):
        """
        TDD-unit test model for the route to validate valid token
        """
        self.mock_response.json.return_value = validate_token_response

        with self.patch:
            res = validate_token()
            assert res == self.mock_response.json.return_value

    def test_validate_faulty_token(self):
        """
        TDD-unit test model for the route to validate token which is faulty
        """

        self.mock_response.json.return_value = {"error": "invalid_token"}

        with self.patch:
            with self.assertRaises(click.ClickException) as context:
                validate_token()

            self.assertIn(
                "Error: invalid_token \nPlease try to log in again.",
                str(context.exception),
            )

    def test_get_profile(self):
        """
        TDD-unit test model for the route to get user profile
        """
        self.mock_response.json.return_value = get_profile_test_response

        with self.patch:
            res = get_profile()
            assert res == self.mock_response.json.return_value

    def test_get_user_ide_courses(self):
        """
        TDD-unit test model for the route, gets all courses user has bookmarked and have ideDocument tag with task paths
        """
        self.mock_response.json.return_value = get_ide_courses_test_response
        validated_value = [Course(**course) for course in get_ide_courses_test_response]

        with self.patch:
            res = get_ide_courses()
            assert res == validated_value

    def test_get_tasks_by_doc(self):
        """
        TDD-unit test model for the route to get tasks by document path
        """
        self.mock_response.json.return_value = get_tasks_by_doc_test_response

        validated_value = [
            TaskData(**task) for task in self.mock_response.json.return_value
        ]

        with self.patch:
            res = get_tasks_by_doc(doc_path="kurssit/testi/test/demot/Demo1")
            assert res == validated_value

    def test_get_task_by_ide_task_id(self):
        """
        TDD-unit test model for the route to get tasks by ideTask id
        """

        self.mock_response.json.return_value = get_task_by_ide_task_id_test_response
        validated_value = TaskData(**self.mock_response.json.return_value)

        with self.patch:
            res = get_task_by_ide_task_id(
                ide_task_id="t1", doc_path="kurssit/testi/test/demot/Demo1"
            )
            assert res == validated_value

    def test_submit_task_by_id(self):
        """
        TDD-unit test model for the route to submit task by task id, document id and paragraph id

        """

        submit_data = submit_task_by_id_test_response
        submit_data = SubmitData(**submit_data)

        self.mock_response.json.return_value = submit_task_by_id_tim_test_response

        with self.patch:
            res = submit_task(submit_data)
            assert res == TimFeedback(
                **self.mock_response.json.return_value.get("result")
            )
