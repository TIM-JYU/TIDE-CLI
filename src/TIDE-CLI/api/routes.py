import requests

from utils.handle_token import get_token


def get_ide_tasks_by_bookmarks(username: str):
    access_token = get_token(username)

    res = requests.get(
        "http://webapp04.it.jyu.fi/oauth/ideTasksByBooksmarks",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    return res.json()
