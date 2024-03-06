import requests

from tidecli.utils.handle_token import get_token

import configparser


def validate_token(username: str):
    """
    Validate the token for the user

    :param username: Username to validate the token for
    return: JSON response  of token time validity
    """
    try:
        access_token = get_token(username)
    except Exception as e:
        print(f"Error getting token: {e}")
        return None

    cf = configparser.ConfigParser()
    cf.read("config.ini")
    base_url = cf["OAuthConfig"]["base_url"]
    validate_token_endpoint = cf["OAuthConfig"]["validate_token_endpoint"]

    res = requests.get(
        f"{base_url}{validate_token_endpoint}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    return res.json()


# def refresh_token():
#     """
#     Refresh the token for the user
#
#     :return: JSON response of the new token
#     """
#     try:
#         access_token = get_token()
#     except Exception as e:
#         print(f"Error getting token: {e}")
#         return None
#
#     cf = configparser.ConfigParser()
#     cf.read("config.ini")
#     base_url = cf["OAuthConfig"]["base_url"]
#     refresh_token_endpoint = cf["OAuthConfig"]["refresh_token_endpoint"]
#
#     res = requests.post(
#         f"{base_url}{refresh_token_endpoint}",
#         headers={"Authorization": f"Bearer {access_token}"},
#     )
#
#     return res.json()
