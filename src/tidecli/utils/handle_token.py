import keyring as kr


def save_token(token, username):
    """
    Save the token in the keyring for the user. Removes the old token if it exists to avoid duplicates.

    :param token: The token to save
    :param username: The username to save the token for
    """
    try:
        kr.delete_password("TIDE", username)
        kr.set_password("TIDE", username, token)
    except Exception as e:
        return f"Error saving token: {e}"


def get_token(username) -> str or None:
    """
    Get the token from the keyring for the user

    :param username: The username to get the token for
    """
    try:
        token = kr.get_password("TIDE", username)
        return token
    except Exception as e:
        print(f"Error getting token: {e}")
        return None
