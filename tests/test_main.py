import unittest
from unittest.mock import patch, MagicMock

from click.testing import CliRunner

from tests.test_data import (
    get_ide_courses_test_response,
    validate_token_response,
    get_tasks_by_doc_test_response,
)
from tests.test_routes import _create_mock_request
from tidecli.main import login, logout, courses, task
from tidecli.models.course import Course
from tidecli.models.user import User


class TestMain(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()

    @patch("tidecli.utils.login_handler.authenticate")
    @patch("keyring.get_password")
    def test_successful_new_login(self, mock_get_password, mock_authenticate):
        mock_get_password.return_value = None
        mock_authenticate.return_value = True
        result = self.runner.invoke(login)
        self.assertEqual(
            result.output,
            "Login successful!\n",
        )

    @patch("tidecli.api.routes.requests.request")
    @patch("keyring.get_password")
    def test_successful_existing_login(self, mock_get_password, mock_request):
        mock_get_password.return_value = "test_token"
        mock_request.return_value = _create_mock_request(validate_token_response)

        result = self.runner.invoke(login)
        self.assertEqual(
            result.output,
            "Logged in as test_token\nToken is still valid for 10 days, 0:00:00\n",
        )

    @patch("tidecli.api.routes.requests.request")
    @patch("keyring.get_password")
    @patch("tidecli.utils.login_handler.authenticate")
    def test_failed_login_invalid_token(
        self, mock_authenticate, mock_get_password, mock_request
    ):
        mock_get_password.return_value = "test_token"
        mock_authenticate.return_value = True
        mock_request.return_value = _create_mock_request({"error": "invalid_token"})

        result = self.runner.invoke(login)
        self.assertEqual(
            result.output,
            "Error: invalid_token\nPlease try to log in again.\nLogin successful!\n",
        )

    @patch("tidecli.main.delete_token")
    def test_logout(self, mock_delete_token):
        return_value = "Token for test deleted successfully!"
        mock_delete_token.return_value = return_value
        result = self.runner.invoke(logout)
        self.assertEqual(result.output, "Token for test deleted successfully!\n")

    @patch("tidecli.api.routes.requests.request")
    @patch("tidecli.api.routes.get_signed_in_user")
    def test_courses(self, mock_get_signed_in_user, mock_request):
        mock_get_signed_in_user.return_value = User("test", "test")
        mock_request.return_value = _create_mock_request(get_ide_courses_test_response)
        validated_value = [Course(**course) for course in get_ide_courses_test_response]
        console_print = "\n".join([course.pretty_print() for course in validated_value])

        result = self.runner.invoke(courses)
        self.assertEqual(result.output, f"{console_print}\n")

    @patch("tidecli.api.routes.requests.request")
    @patch("tidecli.api.routes.get_signed_in_user")
    def test_task_list(self, mock_get_signed_in_user, mock_request):
        mock_get_signed_in_user.return_value = User("test", "test")
        mock_request.return_value = _create_mock_request(get_tasks_by_doc_test_response)

        result = self.runner.invoke(
            task,
            [
                "list",
                "kurssit/tie/ohj2/2024k/demot/DemoC2",
            ],
        )
        self.assertEqual(result.output, "ID: t1\nID: t2\n")

    @patch("tidecli.api.routes.requests.request")
    @patch("tidecli.api.routes.get_signed_in_user")
    def test_task_create_all(self, mock_get_signed_in_user, mock_request):
        mock_get_signed_in_user.return_value = User("test", "test")
        mock_request.return_value = _create_mock_request(get_tasks_by_doc_test_response)

        result = self.runner.invoke(
            task,
            ["create", "kurssit/tie/ohj2/2024k/demot/DemoC2", "t1", "--all"],
        )
        self.assertEqual(
            result.output,
            "Task created in C:\\kurssit\finalcli\\TIDE-CLI\\tests\Demo1\\t1\nTask created in C:\\kurssit\\finalcli\TIDE-CLI\\tests\Demo1\\t2",
        )
