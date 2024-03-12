import os

import requests
import configparser

from tidecli.utils.handle_token import get_signed_in_user


class Routes:
    def __init__(self):
        self.token = None
        self.base_url = None
        self.cf = self.load_config()

    def load_config(self):
        """
        Load the token and base url/endpoint from the config file
        """
        config_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../config.ini")
        )
        cf = configparser.ConfigParser()
        try:
            cf.read(config_path)
            self.base_url = cf["OAuthConfig"]["base_url"]
            token = get_signed_in_user()
            if token is None:
                raise ConfigError("User not logged in")
            # TODO: Better error handling
            self.token = get_signed_in_user().password
            return cf
        except Exception as e:
            print(e)
            raise ConfigError("Config file not found")

    def make_request(self, endpoint: str, method: str = "GET", params: dict = None):
        """
        Make a request to the API

        :param endpoint: API endpoint
        :param method: HTTP method
        :param params: data to send
        return: JSON response
        """

        try:
            res = requests.request(
                method,
                f"{self.base_url}{endpoint}",
                headers={"Authorization": f"Bearer {self.token}"},
                json=params,
            )
            return res.json()

        except requests.exceptions.RequestException as e:
            print(e)
            raise RequestError("Request failed" + str(e))

    def validate_token(self) -> dict:
        """
        Validate the token for the user
        return: JSON response  of token time validity or TODO: This might not work as expected
        """
        endpoint = self.cf["OAuthConfig"]["validate_token_endpoint"]
        return self.make_request(endpoint=endpoint)

    def get_profile(self) -> dict:
        """
        Get the user profile
        return: JSON response  of user profile
        """
        endpoint = self.cf["OAuthConfig"]["profile_endpoint"]
        return self.make_request(endpoint=endpoint)

    def get_ide_courses(self):
        """
        Get the logged in user courses that are in user bookmarks and have ideCourse tag
        return: JSON response of course name and course path, course id and paths for demo documents
        """
        endpoint = self.cf["OAuthConfig"]["ide-courses_endpoint"]
        return self.make_request(endpoint=endpoint)

    def get_demos_by_doc_id(self, doc_id: int):
        """
        Get the demos that are listed in ideDocuments tag in document tags by document id
        :param doc_id: document id
        return: JSON response of demos
        """
        endpoint = self.cf["OAuthConfig"]["demos_by_doc_id_endpoint"]
        return self.make_request(endpoint=endpoint, params={"doc_id": doc_id})

    def get_demos_by_doc_path(self, doc_path: str):
        """
        Get the demos that are listed in ideDocuments tag in document tags by course name
        :param doc_path: Course main document path
        return: JSON response of demos
        """
        endpoint = self.cf["OAuthConfig"]["demos_by_doc_path_endpoint"]
        return self.make_request(endpoint=endpoint, params={"doc_path": doc_path})

    def get_tasks_by_doc_path(self, doc_path: str):
        """
        Get the tasks by demo document path
        :param doc_path: Demo document path
        return: JSON response of tasks
        """
        endpoint = self.cf["OAuthConfig"]["tasks_by_doc_path_endpoint"]
        return self.make_request(endpoint=endpoint, params={"doc_path": doc_path})

    def get_tasks_by_doc_id(self, doc_id: int):
        """
        Get the tasks by demo document id
        :param doc_id: Demo document id
        return: JSON response of tasks
        """
        endpoint = self.cf["OAuthConfig"]["tasks_by_doc_id_endpoint"]
        return self.make_request(endpoint=endpoint, params={"doc_id": doc_id})

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
        endpoint = self.cf["OAuthConfig"]["task_by_ide_task_id_endpoint"]
        return self.make_request(
            endpoint=endpoint,
            params={
                "doc_id": doc_id,
                "doc_path": doc_path,
                "ide_task_id": ide_task_id,
            },
        )


# TODO: Add error handling
class ConfigError(Exception):
    """
    Exception raised for errors in the config file
    """

    pass


class RequestError(Exception):
    """
    Exception raised for errors in the request
    """

    pass
