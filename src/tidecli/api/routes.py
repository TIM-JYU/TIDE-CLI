import click
import requests

from tidecli.models.course import Course
from tidecli.models.submit_data import SubmitData
from tidecli.models.task_data import TaskData
from tidecli.models.tim_feedback import TimFeedback
from tidecli.tide_config import (
    BASE_URL,
    INTROSPECT_ENDPOINT,
    PROFILE_ENDPOINT,
    IDE_COURSES_ENDPOINT,
    TASK_BY_IDE_TASK_ID_ENDPOINT,
    SUBMIT_TASK_ENDPOINT,
    TASKS_BY_DOC_ENDPOINT,
)
from tidecli.utils.handle_token import get_signed_in_user


def make_request(
    endpoint: str, method: str = "GET", params: dict[str, str] | None = None
):
    """
    Make a request to the API

    :param endpoint: API endpoint
    :param method: HTTP method
    :param params: data to send
    return: JSON response
    """

    try:
        token: str = get_signed_in_user().password if get_signed_in_user() else None

        if not token:
            raise click.ClickException("User not logged in")

        res = requests.request(
            method,
            f"{BASE_URL}{endpoint}",
            headers={"Authorization": f"Bearer {token}"},
            json=params,
        )
        return res.json()

    except Exception as e:
        raise click.ClickException("Request failed. " + str(e))


def validate_token() -> dict:
    """
    Validate the token for the user
    return: JSON response  of token validity
    """
    return make_request(endpoint=INTROSPECT_ENDPOINT, method="POST")


def get_profile() -> dict:
    """
    Get the user profile
    return: JSON response  of user profile
    """
    return make_request(endpoint=PROFILE_ENDPOINT)


def get_ide_courses() -> list[Course]:
    """
    Get the logged in user courses that are in user bookmarks and have ideCourse tag
    return: JSON response of course name and course path, course id and paths for demo documents
    """
    res = make_request(endpoint=IDE_COURSES_ENDPOINT)

    if "error" in res:
        raise click.ClickException(res["error"])

    all_courses = [Course(**course) for course in res]

    return all_courses


def get_tasks_by_doc(
    doc_path: str | None = None, doc_id: int | None = None
) -> list[TaskData]:
    """
    Get the tasks by document path or document id
    :param doc_path: Tasks folder path
    :param doc_id: Document id
    return: JSON response of tasks
    """

    if doc_path is None and doc_id is None:
        raise click.ClickException("doc_path or doc_id must be provided")

    res = make_request(
        endpoint=TASKS_BY_DOC_ENDPOINT,
        params={"doc_path": doc_path, "doc_id": doc_id},
    )

    if "error" in res:
        raise click.ClickException(res["error"])

    tasks = [TaskData(**task) for task in res]

    return tasks


def get_task_by_ide_task_id(
    ide_task_id: str,
    doc_path: str | None = None,
    doc_id: int | None = None,
) -> TaskData:
    """
    Get the tasks by ideTask id and demo document path or id
    :param doc_path: Demo document path
    :param ide_task_id: ideTask id
    :param doc_id: Demo document id
    return: JSON response of tasks
    """
    # TODO: muuta funktio toimimaan pelkällä
    # idllä tai pathilla. Ei tarvita molempia
    res = make_request(
        endpoint=TASK_BY_IDE_TASK_ID_ENDPOINT,
        params={
            "doc_id": doc_id,
            "doc_path": doc_path,
            "ide_task_id": ide_task_id,
        },
    )

    if "error" in res:
        raise click.ClickException(res["error"])

    return TaskData(**res)


def submit_task(
    task_files: SubmitData,
) -> TimFeedback:
    """
    Submit the task by task id, document id and paragraph id
    :param task_files: Task/s data
    return: JSON response of tasks
    """

    res = make_request(
        endpoint=SUBMIT_TASK_ENDPOINT, method="PUT", params=task_files.submit_json()
    )

    if "error" in res:
        raise click.ClickException(res["error"])

    return TimFeedback(**res.get("result"))
