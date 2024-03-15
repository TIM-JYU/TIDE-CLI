import unittest

from tidecli.api.routes import Routes
from unittest.mock import patch, MagicMock

# TODO: Saman luokan alle kaikki -> refaktoroi esimerkit yhteen


class TestAuthentication(unittest.TestCase):
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
        user = MagicMock()
        user.id = 1
        user.email = "test@t.fi"
        user.last_name = "Testinen"
        user.given_name = "Teppo"
        user.real_name = "Teppo Testinen"
        user.name = "test"
        self.mock_response.json.return_value = {
            "id": user.id,
            "emails": [
                {
                    "email": user.email,
                    "verified": True,
                }
            ],
            "last_name": user.last_name,
            "given_name": user.given_name,
            "real_name": user.real_name,
            "username": user.name,
        }

        with self.patch:
            res = self.routes.get_profile()
            assert res == self.mock_response.json.return_value

    def test_validate_new_token(self):
        """
        TDD-unit test model for the route to validate new token
        """
        self.mock_response.json.return_value = {"validityTime": "10 days, 0:00:00"}

        return_value = {"validityTime": "10 days, 0:00:00"}

        with self.patch:
            res = self.routes.validate_token()
            assert res == return_value

    def test_validate_token_with_expired_time(self):
        """
        TDD-unit test model for the route to validate token which time has expired
        """
        self.mock_response.json.return_value = {"validityTime": "0:00:00"}

        return_value = {"validityTime": "0:00:00"}

        with self.patch:
            res = self.routes.validate_token()
            assert res == return_value


class TestGetCourse(unittest.TestCase):
    def setUp(self):
        self.routes = Routes()
        self.mock_response = MagicMock()
        self.patch = patch(
            "tidecli.api.routes.requests.request",
            return_value=self.mock_response,
        )

    def test_get_ideTask_courses(self):
        """
        TDD-unit test model for the route, gets all courses user has bookmarked and have ideDocument tag.
        """
        self.mock_response.json.return_value = [
            {
                "course_name": "Ohjelmointi 1",
                "course_path": "/view/courses/ohjelmointi1",
                "document_id": "1",
            },
            {
                "course_name": "Testikurssi 5",
                "course_path": "/view/courses/testikurssi5",
                "document_id": "5",
            },
        ]

        with self.patch:
            res = self.routes.get_ide_courses()
            assert res == self.mock_response.json.return_value


class TestGetDemos(unittest.TestCase):

    def setUp(self):
        self.routes = Routes()
        self.mock_response = MagicMock()
        self.patch = patch(
            "tidecli.api.routes.requests.request",
            return_value=self.mock_response,
        )

    def test_get_demos_by_doc_id(self):
        """
        TDD-unit test model for the route
        """

        # This should return the list of documents in the course with parameter defined in document tag:
        # ideDocuments:
        #   - path: "kurssit/tie/Ohjelmointi2/Demo1
        #   - path: "kurssit/tie/Ohjelmointi2/Demo2
        #   - path: "kurssit/tie/Ohjelmointi2/Demo3
        #   - path: "kurssit/tie/Ohjelmointi2/Demo4
        #   - path: "kurssit/tie/Ohjelmointi2/Demo5

        self.mock_response.json.return_value = {
            "Ohjelmointi2": [
                {
                    "name": "Demo1",
                    "path": "kurssit/tie/Ohjelmointi2/Demo1",
                    "doc_id": 1,
                },
                {
                    "name": "Demo2",
                    "path": "kurssit/tie/Ohjelmointi2/Demo2",
                    "doc_id": 2,
                },
                {
                    "name": "Demo3",
                    "path": "kurssit/tie/Ohjelmointi2/Demo3",
                    "doc_id": 3,
                },
            ]
        }

        with self.patch:
            res = self.routes.get_demos_by_doc_id(doc_id=1)
            assert res == self.mock_response.json.return_value

    def test_get_demos_by_course_name(self):
        """
        TDD-unit test model for the route
        """

        self.mock_response.json.return_value = {
            "Ohjelmointi2": [
                {
                    "name": "Demo1",
                    "path": "kurssit/tie/Ohjelmointi2/Demo1",
                    "doc_id": 1,
                },
                {
                    "name": "Demo2",
                    "path": "kurssit/tie/Ohjelmointi2/Demo2",
                    "doc_id": 2,
                },
                {
                    "name": "Demo3",
                    "path": "kurssit/tie/Ohjelmointi2/Demo3",
                    "doc_id": 3,
                },
            ]
        }

        with self.patch:
            res = self.routes.get_demos_by_doc_path(doc_path="Ohjelmointi2")
            assert res == self.mock_response.json.return_value


class TestGetTasks(unittest.TestCase):
    def setUp(self):
        self.routes = Routes()
        self.mock_response = MagicMock()
        self.patch = patch(
            "tidecli.api.routes.requests.request",
            return_value=self.mock_response,
        )

    def test_get_tasks_by_demo_doc_id(self):
        """
        TDD-unit test model for the route to get tasks by demo doc id
        """

        self.mock_response.json.return_value = {
            "Demo1": [
                # One code file per task, file saved to root of the demo
                {
                    "task_info": {
                        "header": "Tehtävä 1",
                        "stem": "Kirjoita ohjelma, joka tulostaa 'Hello World' konsoliin",
                        "type": "py",
                        "answer_count": 1,
                        "task_id": 1,
                    },
                    "code_files": [
                        {
                            "code": "print('Hello World1')",
                            "path": None,
                            "ideTask_id": "T1",
                            "paragraph_id": "P1",
                        },
                    ],
                }
            ],
            "Demo2": [
                # Multiple code files per task files listed with "files:"-tag and saved according to the path
                {
                    "task_info": {
                        "header": "Tehtävä 1",
                        "stem": "Kirjoita ohjelma joka hakee muuttujan toisesta tiedostosta",
                        "type": ".py",  # Not sure how to get this
                        "answer_count": 1,
                    },
                    "code_files": [
                        {
                            "code": "print('Hello World1')",
                            "path": "/main.py",
                            "ideTask_id": "T1",
                            "paragraph_id": "P1",
                        },
                        {
                            "code": "print('Hello Worlds2')",
                            "path": "/main2.py",
                            "ideTask_id": "T2",
                            "paragraph_id": "P2",
                        },
                    ],
                }
            ],
            "Demo3": [
                # Multiple code files with same ideTask id. Files saved by language specific structure. In this case
                # the files should be saved to the folder Demo3/demo.d3/
                {
                    "task_info": {
                        "header": "Tehtävä 1",
                        "stem": "Write two programs that print 'Hello World' to the console and are in the same java "
                        "package",
                        "type": "java",
                        "answer_count": 0,
                        "task_id": 1,
                    },
                    "code_files": [
                        {
                            "code": "package demo.d3\npublic class Testi {\n\tpublic static void main(String[] args)"
                            '{\nSystem.out.println("Hello World!");\n\t}\n}',
                            "path": None,
                            "ideTask_id": "T1",
                            "paragraph_id": "P1",
                        },
                        {
                            "code": "package demo.d3\npublic class Testi2 {\n\tpublic static void main(String[] args)"
                            '{\nSystem.out.println("Hello World!");\n\t}\n}',
                            "path": None,
                            "ideTask_id": "T1",
                            "paragraph_id": "P1",
                        },
                    ],
                }
            ],
        }

        with self.patch:
            res = self.routes.get_tasks_by_doc_id(doc_id=1)
            assert res == self.mock_response.json.return_value

    def test_get_tasks_by_demo_doc_path(self):
        """
        TDD-unit test model for the route to get tasks by demo doc path
        """

        self.mock_response.json.return_value = {
            "Demo1": [
                # One code file per task, file saved to root of the demo
                {
                    "task_info": {
                        "header": "Tehtävä 1",
                        "stem": "Kirjoita ohjelma, joka tulostaa 'Hello World' konsoliin",
                        "type": "py",
                        "answer_count": 1,
                        "task_id": 1,
                    },
                    "code_files": [
                        {
                            "code": "print('Hello World1')",
                            "path": None,
                            "ideTask_id": "T1",
                            "paragraph_id": "P1",
                        },
                    ],
                }
            ],
        }
        with self.patch:
            res = self.routes.get_tasks_by_doc_path(
                doc_path="kurssit/tie/Ohjelmointi2/Demo1"
            )
            assert res == self.mock_response.json.return_value

    def test_get_task_by_ide_task_id(self):

        self.mock_response.json.return_value = {
            "Demo1": [
                # One code file per task, file saved to root of the demo
                {
                    "task_info": {
                        "header": "Tehtävä 1",
                        "stem": "Kirjoita ohjelma, joka tulostaa 'Hello World' konsoliin",
                        "type": "py",
                        "answer_count": 1,
                        "task_id": 1,
                    },
                    "code_files": [
                        {
                            "code": "print('Hello World1')",
                            "path": None,
                            "ideTask_id": "T1",
                            "paragraph_id": "P1",
                        },
                    ],
                }
            ],
        }

        with self.patch:
            res = self.routes.get_task_by_ide_task_id(
                demo_path="kurssit/tie/Ohjelmointi2/Demo1", ide_task_id="T1"
            )
            assert res == self.mock_response.json.return_value


class TestSubmitTask(unittest.TestCase):

    def test_submit_task_by_id(self):
        # TODO: Submit task by id
        pass
