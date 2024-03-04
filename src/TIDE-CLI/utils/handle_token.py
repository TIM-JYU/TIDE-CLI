import keyring as kr


def save_token(token, username):
    """
    Save the token in the keyring for the user

    :param token: The token to save
    :param username: The username to save the token for
    """
    kr.set_password('TIDE', username, token)


def get_token(username) -> str:
    """
    Get the token from the keyring for the user

    :param username: The username to get the token for
    """
    return kr.get_password('TIDE', username)
