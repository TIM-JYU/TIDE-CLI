import datetime

import click

from tidecli.api.oauth_login import authenticate
from tidecli.api.routes import validate_token
from tidecli.models.user import User
from tidecli.utils.handle_token import get_signed_in_user


def login_details(jsondata: bool = False):
    """
    Get the login details for the user, if the user is already logged in then return the token validity time
    If the user is not logged in then return the login link
    """

    user_login: User | None = get_signed_in_user()

    # If the username exist in credential manager then return the token validity
    if user_login and user_login.password:

        # Validate the token, in case of error in validation, return the error message and ask the user to login again
        try:
            token_validity_time = validate_token()
        except click.ClickException as e:
            click.echo(f"Error: {e}" + "\nPlease try to log in again.")
            if authenticate():
                if jsondata:
                    return {"login_success": True}
                return "Login successful!"
            else:
                if jsondata:
                    return {"login_success": False}
                return "Login failed. Please try again."

        # If the token is not expired then return the token validity time
        expiration_time = token_validity_time.get("exp")
        if expiration_time:
            if jsondata:
                return {
                    "login_success": True,
                }
            return (
                "Logged in as "
                + user_login.username
                + "\nToken is still valid for "
                + str(datetime.timedelta(seconds=expiration_time))
            )
        else:
            if jsondata:
                return {"login_success": False}
            return "Token validity time not found"

    # If the username does not exist in credential manager then return the login link
    else:
        if authenticate():
            if jsondata:
                return {"login_success": True}
            return "Login successful!"
        else:
            return "Login failed. Please try again."
