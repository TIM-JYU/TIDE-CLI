import unittest
from unittest.mock import patch, MagicMock

from tidecli.api.routes import *
from tidecli.models.SubmitData import SubmitData
from tidecli.models.TaskData import TaskFile


class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.routes = Routes()
        self.mock_response = MagicMock()
        self.patch = patch(
            "tidecli.api.routes.requests.request",
            return_value=self.mock_response,
        )

    def test_get_profile(self):
        """
        TDD-unit test model for the route to get user profile
        """
        self.mock_response.json.return_value = {
            'emails': [
                {'email': 't1@test.com',
                 'verified': True}],
            'given_name': 'Testfirstname',
            'id': 2,
            'last_name': 'Testlastname',
            'real_name': 'Tester',
            'username': 'test'
        }

        with self.patch:
            res = self.routes.get_profile()
            assert res == self.mock_response.json.return_value

    def test_validate_token(self):
        """
        TDD-unit test model for the route to validate valid token
        """
        self.mock_response.json.return_value = {
            'active': True,
            'aud': 'oauth2_tide',
            'client_id': 'oauth2_tide',
            'exp': 864000,
            'iat': 123123,
            'scope': 'profile user_tasks user_courses',
            'token_type': 'Bearer',
            'username': 'test'
        }

        with self.patch:
            res = self.routes.validate_token()
            assert res == self.mock_response.json.return_value

    def test_validate_token_with_expired_time(self):
        """
        TDD-unit test model for the route to validate token which time has expired
        """

        # TODO: Confirm this when introspect endpoint is implemented correctly
        self.mock_response.json.return_value = {
            'active': False,
            'aud': 'oauth2_tide',
            'client_id': 'oauth2_tide',
            'exp': 0,
            'iat': 123123,
            'scope': 'profile user_tasks user_courses',
            'token_type': 'Bearer',
            'username': 'test'
        }

        with self.patch:
            res = self.routes.validate_token()
            assert res == self.mock_response.json.return_value

    def test_get_user_ide_courses(self):
        """
        TDD-unit test model for the route, gets all courses user has bookmarked and have ideDocument tag with task paths
        """
        self.mock_response.json.return_value = [
            {
                'id': 58,
                'name': 'Ohjelmointikurssi1',
                'path': '/view/courses/ohjelmointikurssi1/ohjelmointikurssi1',
                'task_paths': ['courses/ohjelmointikurssi1/Demot/Demo1',
                               'courses/ohjelmointikurssi1/Demot/Demo2']
            }
        ]

        with self.patch:
            res = self.routes.get_ide_courses()
            assert res == self.mock_response.json.return_value

    def test_task_folders_by_doc(self):
        """
        TDD-unit test model for the route
        """

        # This should return the list of documents in the course with parameter defined in document tag:
        # ideDocuments:
        #   - path: "kurssit/tie/Ohjelmointi2/DemDemo1"

        self.mock_response.json.return_value = [
            'kurssit/tie/Ohjelmointi2/Demot/Demo1',
            'kurssit/tie/Ohjelmointi2/Demot/Demo2']

        # Test with doc_id
        with self.patch:
            res = self.routes.task_folders_by_doc(doc_id=1)
            assert res == self.mock_response.json.return_value

        # Test with doc_path
        with self.patch:
            res = self.routes.task_folders_by_doc(doc_path="kurssit/tie/Ohjelmointi2/Ohjelmointi2")
            assert res == self.mock_response.json.return_value

    def test_get_tasks_by_doc(self):
        """
        TDD-unit test model for the route to get tasks by task document path or document id
        """

        self.mock_response.json.return_value = [
            # One code file per task
            {
                "task_files": [
                    {
                        "content": "print('Hello world!')",
                        "path": "main.py"
                    }
                ],
                "header": "Tehtävä 1",
                "stem": "Kirjoita viesti maailmalle",
                "type": "py",
                "task_id": "pythontesti",
                "doc_id": 60,
                "par_id": "Xelt2CQGvUwL",
                "ide_task_id": "Tehtävä1"
            },

            # Multiple code files per task files listed with "files:"-tag and saved according to the path
            {
                "task_files": [
                    {
                        "content": "#include <stdio.h>\n#include \"add.h\"\n\nint main() {\n  printf(\"%d\", add(1, 2));\n  return 0;\n}\n",
                        "path": "main.cc"
                    },
                    {
                        "content": "\nint add(int a, int b) {\n  return 0;\n}\n",
                        "path": "add.cc"
                    },
                    {
                        "content": "\nint add(int a, int b);",
                        "path": "add.h"
                    }
                ],
                "header": "Tehtävä 2",
                "stem": "md:\nKorjaa `add.cc`:ssa oleva `add`-funktio niin, että se summaa\nluvut `a` ja `b`.",
                "type": "cc",
                "task_id": "Tehtava3",
                "doc_id": 60,
                "par_id": "RDDZdgS1GwDR",
                "ide_task_id": "Tehtävä2"
            },

            # TODO: Multiple code files with same ideTask id. Files saved by language specific structure.
        ]

        # Test with doc_id
        with self.patch:
            res = self.routes.get_tasks_by_doc(doc_id=1)
            assert res == self.mock_response.json.return_value

        # Test with doc_path
        with (self.patch):
            res = self.routes.get_tasks_by_doc(
                doc_path="kurssit/tie/Ohjelmointi2/Demot/Demo1"
            )
            assert res == self.mock_response.json.return_value

    def test_get_task_by_ide_task_id(self):
        """
        TDD-unit test model for the route to get tasks by ideTask id and demo document path or document id
        """
        self.mock_response.json.return_value = {
            'doc_id': 60,
            'header': 'Tehtävä 5',
            'ide_task_id': 'Tehtävä5',
            'par_id': 'pukg3h0uynFa',
            'stem': 'Hello World -ohjelma tulostaa näytölle tekstin "Hello World".\n',
            'task_files': [
                {'content': 'System.Console.WriteLine("Hello World");', 'path': 'main.cs'}
            ],
            'task_id': 'tehtava5',
            'type': 'cs'
        }

        # Test with doc_path
        with self.patch:
            res = self.routes.get_task_by_ide_task_id(
                doc_path="kurssit/tie/Ohjelmointi2/Demo1", ide_task_id="T1"
            )
            assert res == self.mock_response.json.return_value

        # Test with doc_id
        with self.patch:
            res = self.routes.get_task_by_ide_task_id(
                doc_id=2, ide_task_id="T1"
            )
            assert res == self.mock_response.json.return_value

    def test_submit_task_by_id(self):
        """
        TDD-unit test model for the route to submit task by task id, document id and paragraph id

        """

        code_file = TaskFile(content=f"print('hello world!)", path="main.py")  # TaskFile for single file

        code_files = [
            TaskFile(
                content="#include <stdio.h>\n#include \"add.h\"\n\nint main() {\nprintf(\"%d\", add(1, 2));\nreturn 1;\n}\n",
                path="main.cc"),
            TaskFile(content="int add(int a, int b) {\nreturn 0;\n}\n", path="add.cc"),
            TaskFile(content="int add(int a, int b);", path="add.h")
        ]

        # Submitdata for single file
        t = SubmitData(code_files=code_file, task_id="Tehtava1", doc_id=60, code_language="py")

        # Submitdata for multiple files
        t2 = SubmitData(code_files=code_files, task_id="Tehtava2", doc_id=60, code_language="cc")

        self.mock_response.json.return_value = {
            'plugin': None,
            'result':
                {
                    'savedNew': 81,
                    'valid': True,
                    'web': {
                        'console': 'hello world!\n',
                        'error': '',
                        'language': None,
                        'pwd': '',
                        'runtime': '  0.640   0.616\n\nRun time:\nreal\t0m0.034s\nuser\t0m0.023s\nsys\t0m0.011s\n'
                    }
                }
        }

        with self.patch:
            res = self.routes.submit_task(task_files=t)
            assert res == self.mock_response.json.return_value

        self.mock_response.json.return_value = {
            'plugin': None,
            'result': {
                'savedNew': 81,
                'valid': True,
                'web': {
                    'console': 'Feedback for the task\n',
                    'error': '',
                    'pwd': '',
                    'language': None,
                    'runtime': '  0.640   0.616\n\nRun time:\nreal\t0m0.034s\nuser\t0m0.023s\nsys\t0m0.011s\n'
                },
            },
        }

        with self.patch:
            res = self.routes.submit_task(task_files=t2)
            assert res == self.mock_response.json.return_value
