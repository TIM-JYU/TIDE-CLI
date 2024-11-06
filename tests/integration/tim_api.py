"""
Basic Python API for working with TIM.

.. note:: The API requires you to create a TIM password. 
        If you don't have one (e.g., logged in via Haka), 
        log out of TIM and use "Forgot password" to create one.
"""

__authors__ = ["Denis Zhidkikh, Olli-Pekka Riikola"]
__license__ = "MIT"
__date__ = "2023-03-23"

from enum import Enum
from dotenv import load_dotenv

load_dotenv()

from base64 import b64decode
from datetime import datetime
from email.utils import parsedate_to_datetime
import getpass
import json
from typing import Literal, Optional, overload
import uuid
import zlib
import requests
import os
import urllib.parse
from pydantic.dataclasses import dataclass
from itsdangerous import base64_decode


session: Optional[requests.Session] = None
TIM_DOMAIN = os.environ.get("TIM_DOMAIN", "http://localhost")


def login(username: str, password: str, session: requests.Session) -> None:
    """
    Log in to TIM. Prompts for username and password.

    :param session: Session to use for logging in
    """
    # TIM needs CSRF token for some API calls
    r = session.get(f"{TIM_DOMAIN}")
    csrf_token = r.cookies["XSRF-TOKEN"]
    session.headers.update({"X-XSRF-TOKEN": csrf_token, "Referer": TIM_DOMAIN})

    r = session.post(
        f"{TIM_DOMAIN}/emailLogin",
        data={
            "email": username,
            "password": password,
            "add_user": False,
        },
    )

    if r.status_code != 200:
        raise Exception(f"Login failed: {r.text}")


def get_session() -> requests.Session:
    """
    Get a session for making authenticated requests to TIM.
    If user hasn't logged in yet, prompts for username and password.

    :return: Session for making authenticated requests to TIM
    """
    global session
    if session is None:
        session = requests.Session()
    return session


@dataclass
class PluginType:
    """
    Information about the plugin type
    """

    type: str


@dataclass
class AnswerInfo:
    """
    Information about a user answer
    """

    id: int
    task_id: str
    points: float | None
    answered_on: datetime
    valid: bool
    last_points_modifier: float | None
    plugin: PluginType | None
    content: str | None = None


@dataclass
class UserInfo:
    """
    Information about the user who answered the task
    """

    name: str
    id: int | None = None
    real_name: str | None = None
    email: str | None = None


@dataclass
class AnswerAndUserInfo:
    """
    A single answer entry which contains information about an answer and the user who answered it
    """

    count: int
    user: UserInfo
    answer: AnswerInfo


@dataclass
class ItemInfo:
    """
    Information about a TIM item (document or folder)
    """

    id: int
    type: str
    title: str
    location: str
    short_name: str
    lang_id: str | None = None


def get_item_info(path: str) -> ItemInfo:
    """
    Get information about a TIM item (document or folder).

    :param path: Path to the item

    :return: Information about the item
    """
    session = get_session()
    r = session.get(f"{TIM_DOMAIN}/itemInfo/{path}")
    if r.status_code != 200:
        raise Exception(f"Failed to get item info: {r.text}")
    return ItemInfo(**r.json())


@overload
def get_all_doc_answers(
    doc: int,
    age: str = "max",
    consent: str = "any",
    format: Literal["json"] = "json",
    name: str = "username",
    period: str = "whenever",
    print: str = "all",
    sort: str = "username",
    valid: str = "all",
    group: Optional[str] = None,
    includeInactiveMemberships: bool = False,
) -> list[AnswerAndUserInfo]: ...


@overload
def get_all_doc_answers(
    doc: int,
    age: str = "max",
    consent: str = "any",
    format: Literal["text"] = "text",
    name: str = "username",
    period: str = "whenever",
    print: str = "all",
    sort: str = "username",
    valid: str = "all",
    group: Optional[str] = None,
    includeInactiveMemberships: bool = False,
) -> list[AnswerAndUserInfo]: ...


def get_all_doc_answers(
    doc: int,
    age: str = "max",
    consent: str = "any",
    format: str = "json",
    name: str = "username",
    period: str = "whenever",
    print: str = "all",
    sort: str = "username",
    valid: str = "all",
    group: Optional[str] = None,
    includeInactiveMemberships: bool = False,
) -> str | list[AnswerAndUserInfo]:
    """
    Get all answers to all tasks that are located in a document.

    :param doc: ID of the document
    :param age: Age of the answers to get.
    :param consent: Whether to only get answers from users who have given consent.
    :param format: Format of the returned data. Can be either "json" or "text".
    :param name: How to display the user names.
    :param period: Period of the answers to get.
    :param print: What information to include in the returned data.
    :param sort: How to sort the returned data.
    :param valid: What validity status to include in the returned data.
    :param group: Group to get answers from.
    :param includeInactiveMemberships: Whether to include inactive group members in the returned data.

    :return: Answers to all tasks in the document
    """
    session = get_session()

    params = {
        "age": age,
        "consent": consent,
        "format": format,
        "name": name,
        "period": period,
        "print": print,
        "sort": sort,
        "valid": valid,
        "includeInactiveMemberships": includeInactiveMemberships,
    }

    if group is not None:
        params["group"] = group

    # Convert params to URL query string
    url_params = urllib.parse.urlencode(params)

    r = session.get(
        f"{TIM_DOMAIN}/allDocumentAnswersPlain/{doc}?{url_params}",
    )

    if r.status_code != 200:
        raise Exception(f"Failed to get answers: {r.text}")

    if format != "json":
        return r.text

    json_data = r.json()
    result = [AnswerAndUserInfo(**x) for x in json_data]

    return result


# TODO: Merge with get_all_doc_answers


@overload
def get_all_task_answers(
    task_id: str,
    age: str = "max",
    consent: str = "any",
    format: Literal["json"] = "json",
    name: str = "username",
    period: str = "whenever",
    print: str = "all",
    sort: str = "username",
    valid: str = "all",
    group: Optional[str] = None,
    includeInactiveMemberships: bool = False,
) -> list[AnswerAndUserInfo]: ...


@overload
def get_all_task_answers(
    task_id: str,
    age: str = "max",
    consent: str = "any",
    format: Literal["text"] = "text",
    name: str = "username",
    period: str = "whenever",
    print: str = "all",
    sort: str = "username",
    valid: str = "all",
    group: Optional[str] = None,
    includeInactiveMemberships: bool = False,
) -> str: ...


def get_all_task_answers(
    task_id: str,
    age: str = "max",
    consent: str = "any",
    format: str = "json",
    name: str = "username",
    period: str = "whenever",
    print: str = "all",
    sort: str = "username",
    valid: str = "all",
    group: Optional[str] = None,
    includeInactiveMemberships: bool = False,
) -> str | list[AnswerAndUserInfo]:
    """
    Get all answers to a task.

    :param task_id: ID of the task. Must be of format DOCID.TASKNAME
    :param age: Age of the answers to get.
    :param consent: Whether to only get answers from users who have given consent.
    :param format: Format of the returned data. Can be either "json" or "text".
    :param name: How to display the user names.
    :param period: Period of the answers to get.
    :param print: What information to include in the returned data.
    :param sort: How to sort the returned data.
    :param valid: What validity status to include in the returned data.
    :param group: Group to get answers from.
    :param includeInactiveMemberships: Whether to include inactive group members in the returned data.

    :return: Answers to the task
    """
    session = get_session()

    params = {
        "age": age,
        "consent": consent,
        "format": format,
        "name": name,
        "period": period,
        "print": print,
        "sort": sort,
        "valid": valid,
        "includeInactiveMemberships": includeInactiveMemberships,
    }

    if group is not None:
        params["group"] = group

    # Convert params to URL query string
    url_params = urllib.parse.urlencode(params)

    r = session.get(
        f"{TIM_DOMAIN}/allAnswersPlain/{task_id}?{url_params}",
    )

    if r.status_code != 200:
        raise Exception(f"Failed to get answers: {r.text}")

    if format != "json":
        return r.text

    json_data = r.json()
    result = [AnswerAndUserInfo(**x) for x in json_data]

    return result


@dataclass
class TaskInfo:
    """
    Information about the task.
    """

    maxPoints: float | None
    userMin: float | None
    userMax: float | None
    showPoints: dict
    deadline: datetime | None
    starttime: datetime | None
    answerLimit: int | None
    triesText: str
    pointsText: str
    buttonNewTask: str | None
    modelAnswer: str | None


def get_task_info_from_doc(doc_path: str, task_name: str) -> tuple[str, TaskInfo]:
    """
    Resolve task ID and task info from a document path and task name.

    :param doc_path: Path to the document
    :param task_name: Name of the task (as defined in the markup)

    :return: Tuple of full task ID and task info
    """
    doc_info = get_item_info(doc_path)
    session = get_session()

    task_id = f"{doc_info.id}.{task_name}"

    r = session.get(
        f"{TIM_DOMAIN}/taskinfo/{task_id}",
    )

    if r.status_code != 200:
        raise Exception(f"Failed to get task info: {r.text}")

    return task_id, TaskInfo(**r.json())


def save_answer_points(user_id: int, answer_id: int, points: float | None) -> None:
    """
    Save the points of an answer.

    :param user_id: ID of the user
    :param answer_id: ID of the answer
    :param points: Points to save
    """
    session = get_session()

    r = session.put(
        f"{TIM_DOMAIN}/savePoints/{user_id}/{answer_id}",
        json={
            "points": points,
        },
    )

    if r.status_code != 200:
        raise Exception(f"Failed to save answer points: {r.text}")

    status = r.json()

    if status.get("status") != "ok":
        raise Exception(f"Failed to save answer points: {status}")


@dataclass
class CurrentUser:
    """
    Information about the current user.
    """

    user_id: int
    user_name: str


def get_current_user() -> CurrentUser:
    """
    Get information about the current logged-in user.
    """

    def decode(cookie):
        try:
            compressed = False
            payload = cookie

            if payload.startswith("."):
                compressed = True
                payload = payload[1:]

            data = payload.split(".")[0]

            data = base64_decode(data)
            if compressed:
                data = zlib.decompress(data)

            return data.decode("utf-8")
        except Exception as e:
            return "[Decoding error: are you sure this was a Flask session cookie? {}]".format(
                e
            )

    def flask_loads(value):
        def object_hook(obj):
            if len(obj) != 1:
                return obj
            the_key, the_value = next(obj.iteritems())
            if the_key == " t":
                return str(tuple(the_value))
            elif the_key == " u":
                return str(uuid.UUID(the_value))
            elif the_key == " b":
                return str(b64decode(the_value))
            elif the_key == " m":
                return str(the_value)
            elif the_key == " d":
                return str(parsedate_to_datetime(the_value))
            return obj

        return json.loads(value, object_hook=object_hook)

    session = get_session()

    sess_cookie = session.cookies.get("session")
    decoded = decode(sess_cookie)
    data = flask_loads(decoded)

    return CurrentUser(**data)


def submit_new_answer(task_id: str, input: dict) -> dict:
    """
    Submit a new answer to a task.

    :param task_id: ID of the task. Must be of format DOCID.TASKNAME
    :param input: Input to submit. Must follow the task's input schema.

    :return: Information about the answer
    """
    session = get_session()
    r = session.put(
        f"{TIM_DOMAIN}/submit/{task_id}/answer",
        json={
            "abData": {},
            "input": input,
        },
    )

    if r.status_code != 200:
        raise Exception(f"Failed to submit new answer: {r.text}")

    return r.json()


def get_group_members(group_name: str) -> list[UserInfo]:
    """
    Get all members of a group.

    :param group_name: Name of the group

    :return: List of group members
    """
    session = get_session()
    r = session.get(
        f"{TIM_DOMAIN}/groups/show/{group_name}",
    )

    if r.status_code != 200:
        raise Exception(f"Failed to get group members: {r.text}")
    json = r.json()
    return [UserInfo(**x) for x in json]


def get_document_markdown(doc_id: int) -> str:
    session = get_session()
    r = session.get(
        f"{TIM_DOMAIN}/download/{doc_id}",
    )

    if r.status_code != 200:
        raise Exception(f"Failed to get document markdown: {r.text}")
    return r.text


def edit_paragraph(doc_id: int, par_id: str, text: str) -> None:
    session = get_session()
    r = session.post(
        f"{TIM_DOMAIN}/postParagraph",
        json={
            "docId": doc_id,
            "par": par_id,
            "tags": {"markread": False},
            "text": text,
            "view": "view",
        },
    )

    if r.status_code != 200:
        raise Exception(f"Failed to post paragraph: {r.text}")

    return r.json()


def add_paragraph(doc_id: int, text: str) -> None:
    session = get_session()

    r = session.post(
        f"{TIM_DOMAIN}/newParagraph",
        json={
            "docId": doc_id,
            "tags": {"markread": False},
            "text": text,
            "view": "view",
        },
    )

    if r.status_code != 200:
        raise Exception(f"Failed to post paragraph: {r.text}")

    return r.json()


def get_par(doc_id: int, par_id: str) -> str:
    session = get_session()

    r = session.get(
        f"{TIM_DOMAIN}/getBlock/{doc_id}/{par_id}",
    )

    if r.status_code != 200:
        raise Exception(f"Failed to get paragraph: {r.text}")

    return r.json()["text"]


class ItemType(Enum):
    Folder = "folder"
    Document = "document"


def create_item(
    item_type: ItemType,
    item_path: str,
    title: str,
) -> None:
    """
    Create a new item in TIM at the specified path.

    .. note:: The child folders will be created automatically.
    .. note:: Item path must use "/" as a separator.

    :param item_type: Type of the item to create.
    :param item_path: Path to the item.
    :param title: Title of the item.
    """
    session = get_session()

    r = session.post(
        f"{TIM_DOMAIN}/createItem",
        json={
            "item_type": item_type.value,
            "item_path": item_path,
            "item_title": title,
        },
    )

    if r.status_code != 200:
        raise Exception(f"Could not to create item: ({r.status_code}), {r.text}")


def create_or_get_item(
    item_type: ItemType,
    item_path: str,
) -> ItemInfo:
    """
    A basic helper to create or get an existing item in TIM at the specified path.
    Item's name is deduced from the last part of the path.

    .. note:: The child folders will be created automatically.
    .. note:: Item path must use "/" as a separator.

    :param item_type: Type of the item to create.
    :param item_path: Path to the item.

    :return: Information about the item.
    """

    try:
        item_info = get_item_info(item_path)
    except Exception:
        create_item(item_type, item_path, item_path.split("/")[-1])
        item_info = get_item_info(item_path)

    return item_info


def upload_markdown(doc_path: str, markdown: str) -> None:
    """
    Upload markdown to a document.
    Any existing markdown will be overwritten.

    :param doc_path: Path to the document
    :param markdown: Markdown to upload
    """

    try:
        item_info = get_item_info(doc_path)
    except Exception as e:
        raise Exception(f"Could not get item info for {doc_path}") from e

    if item_info.type != ItemType.Document.value:
        raise Exception(f"Item at {doc_path} is not a document")

    # It seems that current markdown is needed for some kind of validation/concurrent editing
    current_markdown = get_document_markdown(item_info.id)

    session = get_session()

    r = session.post(
        f"{TIM_DOMAIN}/update/{item_info.id}",
        json={
            "fulltext": markdown,
            "original": current_markdown,
        },
    )

    if r.status_code != 200:
        raise Exception(f"Failed to update document: {r.status_code}, {r.text}")


def add_document_to_my_courses(doc_path: str) -> None:
    session = get_session()

    r = session.post(
            f"{TIM_DOMAIN}/bookmarks/add",
            json = {
                "group": "My courses",
                "link": f"/view/{doc_path}",
                "name": doc_path
                }
            )

    if r.status_code != 200:
        raise Exception(f"Failed to add document to bookmarks: {r.status_code}, {r.text}")
