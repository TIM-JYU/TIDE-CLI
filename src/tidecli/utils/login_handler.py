import datetime

from tidecli.api.oauth_login import authenticate
from tidecli.api.routes import Routes
from tidecli.utils.handle_token import get_signed_in_user


def login_details():
    """
    Get the login details for the user, if the user is already logged in then return the token validity time
    If the user is not logged in then return the login link
    """

    user_login = get_signed_in_user()

    # If the username exist in credential manager then return the token validity
    if user_login:

        token_validity_time = Routes().validate_token()

        # If the token is expired or returns error message TODO: test this
        if token_validity_time.get("error"):
            if authenticate():
                return "Login successful!"
            else:
                return "Login failed. Please try again." + token_validity_time.get("error")

        # If the token is not expired then return the token validity time
        expiration_time = token_validity_time.get("exp")
        if expiration_time:
            return ("Logged in as " + user_login.username +
                    "\nToken is still valid for " + str(datetime.timedelta(seconds=expiration_time)))
        else:
            return "Token validity time not found"

    # If the username does not exist in credential manager then return the login link
    else:
        if authenticate():
            return "Login successful!"
        else:
            return "Login failed. Please try again."