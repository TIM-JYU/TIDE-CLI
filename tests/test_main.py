import unittest
from unittest.mock import patch, MagicMock

from click.testing import CliRunner

from tests.test_data import get_ide_courses_test_response, validate_token_response
from tidecli.main import login, logout, courses
from tidecli.models.course import Course
from tidecli.models.user import User


class TestMain(unittest.TestCase):

    def setUp(self):
        self.mm = MagicMock()
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
        self.mm.json.return_value = validate_token_response
        mock_request.return_value = self.mm

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
        self.mm.json.return_value = {"error": "invalid_token"}
        mock_request.return_value = self.mm
        result = self.runner.invoke(login)
        self.assertEqual(
            result.output,
            "Error: invalid_token\nPlease try to log in again.\nLogin successful!\n",
        )

    @patch("tidecli.main.delete_token")
    def test_logout(self, mock_delete_token):
        ret_value = "Token for test deleted successfully!"
        mock_delete_token.return_value = ret_value
        result = self.runner.invoke(logout)
        self.assertEqual(result.output, "Token for test deleted successfully!\n")
