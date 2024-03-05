from dataclasses import dataclass

import keyring as kr

import configparser


def get_current_username() -> str:
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config.get('User', 'username')

    except (configparser.NoSectionError, configparser.NoOptionError, FileNotFoundError) as e:
        print(f"Error: {e}")
    return ""


@dataclass
class LoginHandler:
    username: str = None
    token: str = None
    config_path: str = 'user_info.ini'

    def __post_init__(self):
        try:
            cf = configparser.ConfigParser()
            self.config = cf.read(self.config_path)
            username = cf.get('User', 'username')
            if username != "":
                self.username = username
                self.token = kr.get_password("TIDE", self.username)

        except (configparser.NoSectionError, configparser.NoOptionError, FileNotFoundError) as e:
            print(f"Error: {e}")

    def is_logged_in(self) -> bool:
        if self.token is not None:
            return True
        return False

    def save_username(self, username: str):
        try:
            config = configparser.ConfigParser()
            config['User'] = {'username': username}
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
        except Exception as e:
            print(f"Error: {e}")

    def save_token_to_user(token, username):
        """
        Save the token in the keyring for the user

        :param token: The token to save
        :param username: The username to save the token for
        """
        try:
            # Remove the token if it already exists to avoid duplicates
            if kr.get_password("TIDE", "username"):
                kr.delete_password("TIDE", "username")

            kr.set_password("TIDE", username, token)
        except Exception as e:
            return f"Error saving token: {e}"

    def username_has_token(username: str) -> bool:
        """
        Check if the token exists for the user

        :param username: The username to check the token for
        """
        return kr.get_password("TIDE", username) is not None

    def remove_token(username: str):
        """
        Remove the token from the keyring for the user

        :param username: The username to remove the token for
        """
        kr.delete_password("TIDE", username)
