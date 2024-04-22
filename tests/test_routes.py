import unittest
from unittest.mock import patch, MagicMock

from tidecli.api.routes import *
from tidecli.models.course import CourseTask
from tidecli.models.task_data import TaskFile


class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.mock_response = MagicMock()
        self.patch = patch(
            "tidecli.api.routes.requests.request", return_value=self.mock_response
        )
        self.mock_response.side_effect = click.ClickException("Error message")

    def test_validate_token(self):
        """
        TDD-unit test model for the route to validate valid token
        """
        self.mock_response.json.return_value = {
            "active": True,
            "client_id": "oauth2_tide",
            "token_type": "Bearer",
            "username": "test_user",
            "scope": "profile user_tasks user_courses",
            "aud": "oauth2_tide",
            "exp": 864000,
            "iat": 1713772959,
        }

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
        self.mock_response.json.return_value = {
            "id": 11111111,
            "emails": [{"email": "test@test.fi", "verified": True}],
            "last_name": "Test",
            "given_name": "Test",
            "real_name": "Test Test",
            "username": "test_user",
        }

        with self.patch:
            res = get_profile()
            assert res == self.mock_response.json.return_value

    def test_get_user_ide_courses(self):
        """
        TDD-unit test model for the route, gets all courses user has bookmarked and have ideDocument tag with task paths
        """
        self.mock_response.json.return_value = [
            {
                "name": "Testikurssi",
                "id": 111111,
                "path": "kurssit/testi/test/",
                "tasks": [
                    {
                        "name": "Demo1",
                        "path": "kurssit/testi/test/demot/Demo1",
                        "doc_id": 1111111,
                    },
                    {
                        "name": "Demo2",
                        "path": "kurssit/testi/test/demot/Demo2",
                        "doc_id": 2222222,
                    },
                ],
            }
        ]
        validated_value = [
            Course(
                name="Testikurssi",
                id=111111,
                path="kurssit/testi/test/",
                tasks=[
                    CourseTask(
                        name="Demo1",
                        doc_id=1111111,
                        path="kurssit/testi/test/demot/Demo1",
                    ),
                    CourseTask(
                        name="Demo2",
                        doc_id=2222222,
                        path="kurssit/testi/test/demot/Demo2",
                    ),
                ],
            )
        ]

        with self.patch:
            res = get_ide_courses()
            assert res == validated_value

    def test_get_tasks_by_doc(self):
        """
        TDD-unit test model for the route to get tasks by document path
        """
        self.mock_response.json.return_value = [
            {
                "task_files": [
                    {
                        "task_id_ext": "111.test.test",
                        "content": '#include <stdio.h>\n\nvoid ohjeet(void)\n{\n  printf("Ohjelma laskee huoneen '
                        'pinta-alan ja tilavuuden annettujen tietojen perusteella.");\n\n}\n\n/* Kirjoita '
                        "tarvittavat aliohjelmat */\n\nint main(void)\n{\n  ohjeet();\n\n  /* Täydennä "
                        "ohjelman toiminta */\n\n  return 0;\n}",
                        "file_name": "test.c",
                        "user_input": "3 4 2.5",
                        "user_args": "",
                    }
                ],
                "path": "kurssit/testi/test/demot/Demo1",
                "header": None,
                "stem": None,
                "type": "cc/input/comtest",
                "task_id": "testi",
                "doc_id": 1,
                "par_id": "asd",
                "ide_task_id": "t2",
            },
        ]

        validated_value = [
            TaskData(
                path="kurssit/testi/test/demot/Demo1",
                type="cc/input/comtest",
                doc_id=1,
                ide_task_id="t2",
                task_files=[
                    TaskFile(
                        task_id_ext="111.test.test",
                        content='#include <stdio.h>\n\nvoid ohjeet(void)\n{\n  printf("Ohjelma laskee huoneen pinta-alan ja tilavuuden annettujen tietojen perusteella.");\n\n}\n\n/* Kirjoita tarvittavat aliohjelmat */\n\nint main(void)\n{\n  ohjeet();\n\n  /* Täydennä ohjelman toiminta */\n\n  return 0;\n}',
                        file_name="test.c",
                        source="editor",
                        user_input="3 4 2.5",
                        user_args="",
                    )
                ],
                stem=None,
                header=None,
            )
        ]

        with self.patch:
            res = get_tasks_by_doc(doc_path="kurssit/testi/test/demot/Demo1")
            assert res == validated_value

    def test_get_task_by_ide_task_id(self):
        """
        TDD-unit test model for the route to get tasks by ideTask id
        """

        self.mock_response.json.return_value = {
            "task_files": [
                {
                    "task_id_ext": "11.test.test",
                    "content": '#include <stdio.h>\n\nvoid ohjeet(void)\n{\n  printf("Ohjelma laskee huoneen '
                    'pinta-alan ja tilavuuden annettujen tietojen perusteella.");\n\n}\n\n/* Kirjoita '
                    "tarvittavat aliohjelmat */\n\nint main(void)\n{\n  ohjeet();\n\n  /* Täydennä "
                    "ohjelman toiminta */\n\n  return 0;\n}",
                    "file_name": "test.c",
                    "user_input": "3 4 2.5",
                    "user_args": "",
                }
            ],
            "path": "kurssit/testi/test/demot/Demo1",
            "header": None,
            "stem": None,
            "type": "cc/input/comtest",
            "task_id": "test",
            "doc_id": 1,
            "par_id": "asd",
            "ide_task_id": "t1",
        }
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

        submit_data = {
            "code_files": [
                {
                    "task_id_ext": "1111.test.asd",
                    "content": '#include <stdio.h>\n\nint main(void)\n{\n  printf("Hello, World!\\n");\n\n  return '
                    "0;\n}",
                    "file_name": "test.c",
                    "source": "editor",
                    "user_input": "",
                    "user_args": "",
                }
            ],
            "code_language": "cc",
        }
        submit_data = SubmitData(**submit_data)

        self.mock_response.json.return_value = {
            "result": {
                "web": {
                    "console": "Hello, World!\n",
                    "error": "",
                    "pwd": "",
                    "language": None,
                    "runtime": "0.883   0.872\nCompile time:\nreal\t0m0.105s\nuser\t0m0.039s\nsys\t0m0.022s\n\nRun "
                    "time:\nreal\t0m0.001s\nuser\t0m0.001s\nsys\t0m0.000s\n",
                },
                "savedNew": 111111,
                "valid": True,
            },
            "plugin": None,
        }

        with self.patch:
            res = submit_task(submit_data)
            assert res == TimFeedback(
                **self.mock_response.json.return_value.get("result")
            )
