from tidecli.api.oauth_login import authenticate
from tidecli.api.routes import validate_token
from tidecli.utils.handle_token import get_signed_in_user


def login_details():
    """
    Get the login details for the user, if the user is already logged in then return the token validity time
    If the user is not logged in then return the login link
    """

    user_login = get_signed_in_user()

    # If the username exist in credential manager then return the token validity
    if user_login:

        token_validity_time = validate_token(user_login.password)

        # If the token is expired then return the message
        # TODO: confirm that token time cannot go negative or below 0:00:00
        if token_validity_time.get("validityTime") == "0:00:00":
            if authenticate():
                return "Login successful! You can now close the browser."
            else:
                return "Login failed. Please try again."

        # If the token is not expired then return the token validity time
        return "Token is still valid for " + token_validity_time.get("validityTime")
