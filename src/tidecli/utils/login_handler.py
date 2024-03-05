import configparser

from tidecli.api.routes import validate_token
from tidecli.utils.handle_token import get_token


def get_signed_user() -> str or None:
    """
    Get the current username from the config file and verifies that user token is valid. Returns token validity time.
    Returns None if the username is not found.
    """
    try:
        user_info = configparser.ConfigParser()
        user_info.read("user_info.ini")
        username = user_info.get("User", "username")
    except (
        configparser.NoSectionError,
        configparser.NoOptionError,
        FileNotFoundError,
    ) as e:
        print(f"Error: {e}")
        return None

    token = get_token(username)

    if token is None:
        return None

    token_validity = validate_token(username)

    # TODO: Tarkista tokenin voimassaoloaika

    return {"username": username, "token_validity": token_validity}


# Jos haluaa toteuttaa luokalla, ehkä turhaa..
# @dataclass
# class LoginHandler:
#     username: str = None
#     token: str = None
#     config_path: str = "user_info.ini"
#
#     def __post_init__(self):
#         try:
#             cf = configparser.ConfigParser()
#             self.config = cf.read(self.config_path)
#             username = cf.get("User", "username")
#             if username != "":
#                 self.username = username
#                 self.token = kr.get_password("TIDE", self.username)
#
#         except (
#             configparser.NoSectionError,
#             configparser.NoOptionError,
#             FileNotFoundError,
#         ) as e:
#             print(f"Error: {e}")
#
#     def is_logged_in(self) -> bool:
#         if self.token is not None:
#             return True
#         return False
#
#     def save_username(self, username: str):
#         try:
#             config = configparser.ConfigParser()
#             config["User"] = {"username": username}
#             with open("config.ini", "w") as configfile:
#                 config.write(configfile)
#         except Exception as e:
#             print(f"Error: {e}")
#
#     def save_token_to_user(token, username):
#         """
#         Save the token in the keyring for the user
#
#         :param token: The token to save
#         :param username: The username to save the token for
#         """
#         try:
#             # Remove the token if it already exists to avoid duplicates
#             if kr.get_password("TIDE", "username"):
#                 kr.delete_password("TIDE", "username")
#
#             kr.set_password("TIDE", username, token)
#         except Exception as e:
#             return f"Error saving token: {e}"
#
#     def username_has_token(username: str) -> bool:
#         """
#         Check if the token exists for the user
#
#         :param username: The username to check the token for
#         """
#         return kr.get_password("TIDE", username) is not None
#
#     def remove_token(username: str):
#         """
#         Remove the token from the keyring for the user
#
#         :param username: The username to remove the token for
#         """
#         kr.delete_password("TIDE", username)
