import click
import keyring as kr
from tidecli.models.user import User


def save_token(token: str, username: str) -> str | None:
    """
    Save the token in the keyring for the user. Removes the old token if it exists to avoid duplicates.

    :param token: The token to save
    :param username: The username to save the token for
    """
    try:
        credentials = kr.get_password("TIDE", "username")
        if credentials:
            # Remove the old token if it exists to avoid duplicates
            delete_token()

        kr.set_password("TIDE", "username", username)
        kr.set_password("TIDE", username, token)
        return None

    except Exception as e:
        raise click.ClickException(f"Error saving token: {e}")


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


def get_signed_in_user() -> User | None:
    """
    Get the signed in user from the keyring

    return: The signed in user username and token
    """
    try:
        username = kr.get_password("TIDE", "username")
        if not username:
            return None
        password = kr.get_password("TIDE", username)
        if not password:
            return None

        user = User(username, password)

        return user

    except Exception as e:
        print(f"Error getting signed in user: {e}")
        return None


def delete_token() -> str | None:
    """
    Delete the token from the keyring for the user
    when log out is called
    """
    try:
        user = get_signed_in_user()
        if user:
            kr.delete_password("TIDE", user.username)
            kr.delete_password("TIDE", "username")
            return f"Token for {user.username} deleted successfully."
        else:
            return "User not logged in."
    except Exception as e:
        raise click.ClickException(f"Error deleting token: {e}")
