from dataclasses import dataclass

import requests

from tidecli.models import SubmitData
from tidecli.tide_config import *
from tidecli.utils.error_logger import error_handler, CliError
from tidecli.utils.handle_token import get_signed_in_user


@error_handler
@dataclass
class Routes:

    token: str = get_signed_in_user().password if get_signed_in_user() else None

    def make_request(self, endpoint: str, method: str = "GET", params: dict = None):
        """
        Make a request to the API

        :param endpoint: API endpoint
        :param method: HTTP method
        :param params: data to send
        return: JSON response
        """

        try:
            if not self.token:
                raise CliError("User not logged in")

            res = requests.request(
                method,
                f"{BASE_URL}{endpoint}",
                headers={"Authorization": f"Bearer {self.token}"},
                json=params,
            )
            return res.json()

        except Exception as e:
            raise CliError("Request failed. " + str(e))

    def validate_token(self) -> dict:
        """
        Validate the token for the user
        return: JSON response  of token validity
        """
        return self.make_request(endpoint=INTROSPECT_ENDPOINT, method="POST")

    def get_profile(self) -> dict:
        """
        Get the user profile
        return: JSON response  of user profile
        """
        return self.make_request(endpoint=PROFILE_ENDPOINT)

    def get_ide_courses(self):
        """
        Get the logged in user courses that are in user bookmarks and have ideCourse tag
        return: JSON response of course name and course path, course id and paths for demo documents
        """
        return self.make_request(endpoint=IDE_COURSES_ENDPOINT)

    def task_folders_by_doc(self, doc_path: str = None, doc_id: int = None):
        """
        Get the course task folders by document path or document id
        :param doc_path: Course main document path
        :param doc_id: Course main document id
        return: JSON response of demos
        """

        if doc_path is None and doc_id is None:
            raise CliError("doc_path or doc_id must be provided")

        return self.make_request(endpoint=TASK_FOLDERS_BY_DOC_ENDPOINT, params={"doc_path": doc_path, "doc_id": doc_id})

    def get_tasks_by_doc(self, doc_path: str = None, doc_id: int = None):
        """
        Get the tasks by document path or document id
        :param doc_path: Tasks folder path
        :param doc_id: Document id
        return: JSON response of tasks
        """

        if doc_path is None and doc_id is None:
            raise CliError("doc_path or doc_id must be provided")

        return self.make_request(endpoint=TASKS_BY_DOC_ENDPOINT, params={"doc_path": doc_path, "doc_id": doc_id})

    def get_task_by_ide_task_id(
            self,
            ide_task_id: str,
            doc_path: str = None,
            doc_id: int = None,
    ):
        """
        Get the tasks by ideTask id and demo document path or id
        :param doc_path: Demo document path
        :param ide_task_id: ideTask id
        :param doc_id: Demo document id
        return: JSON response of tasks
        """

        return self.make_request(
            endpoint=TASK_BY_IDE_TASK_ID_ENDPOINT,
            params={
                "doc_id": doc_id,
                "doc_path": doc_path,
                "ide_task_id": ide_task_id,
            },
        )

    def submit_task(
            self,
            task_file: SubmitData,
    ):
        """
        Submit the task by task id, document id and paragraph id
        :param task_file: Task data
        return: JSON response of tasks
        """

        return self.make_request(
            endpoint=SUBMIT_TASK_ENDPOINT,
            params=task_file.submit_json()
        )
