import keyring as kr


def save_token(token, username):
    """
    Save the token in the keyring for the user. Removes the old token if it exists to avoid duplicates.

    :param token: The token to save
    :param username: The username to save the token for
    """
    try:
        credentials = kr.get_credential("TIDE", None)
        if credentials:
            # Remove the old token if it exists to avoid duplicates
            kr.delete_password("TIDE", credentials.username)
        kr.set_password("TIDE", username, token)

    except Exception as e:
        return f"Error saving token: {e}"


def get_token(username) -> str | None:
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


def get_signed_in_user() -> str | None:
    """
    Get the signed in user from the keyring

    return: The signed in user username and token
    """
    try:
        return kr.get_credential("TIDE", None)
    except Exception as e:
        print(f"Error getting signed in user: {e}")
        return None


def delete_token():
    """
    Delete the token from the keyring for the user
    when log out is called
    """
    try:
        user_name = get_signed_in_user()
        if user_name:
            kr.delete_password("TIDE", user_name.username)
            return f"Token for {user_name.username} deleted successfully."
        else:
            return "User not logged in."
    except Exception as e:
        print(f"Error deleting token: {e} ")
        return None
