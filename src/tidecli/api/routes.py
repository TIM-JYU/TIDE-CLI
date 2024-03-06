import requests
import configparser

from tidecli.utils.handle_token import get_signed_in_user


def validate_token(token: str):
    """
    Validate the token for the user

    :param token: token to validate
    return: JSON response  of token time validity
    """

    cf = configparser.ConfigParser()
    cf.read("config.ini")
    base_url = cf["OAuthConfig"]["base_url"]
    validate_token_endpoint = cf["OAuthConfig"]["validate_token_endpoint"]

    res = requests.get(
        f"{base_url}{validate_token_endpoint}",
        headers={"Authorization": f"Bearer {token}"},
    )

    return res.json()


def get_user_task_by_taskId(task_id: str, doc_id: int):
    """
    Get the user task by task id

    :param doc_id: document id
    :param task_id: task id
    return: JSON response  of user task
    """

    cf = configparser.ConfigParser()
    cf.read("config.ini")
    base_url = cf["OAuthConfig"]["base_url"]
    endpoint = cf["OAuthConfig"]["ide_task_by_taskId_endpoint"]

    token = get_signed_in_user().password

    # ide_task_by_taskId_endpoint = /ide-task-by-id/<int:doc_id>/<string:ide_task_id>
    endpoint.format(doc_id=doc_id, ide_task_id=task_id)

    res = requests.get(
        f"{base_url}{endpoint}/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    return res.json()
