"""Basic error handling and logging for the CLI application."""

authors = ["Olli-Pekka Riikola, Olli Rutanen, Joni Sinokki"]
license = "MIT"
date = "11.5.2024"

import logging
import click

# Configure logger
logging.basicConfig(
    filename="tide-cli.log",
    filemode="a",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def error_handler(func):
    """
    Handle CLI errors.

    This is used as decorator @error_handler
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Log the error
            logging.error(f"Error in function {func.__name__}: {e}")
            # You can add more actions here,
            # like sending an email notification or
            # printing the error to console

            # For simplicity, I'm just re-raising the error here
            # raise
            print("\033[91m {}\033[00m".format(e))

    return wrapper


# TODO: Add error handling for specific errors
class CliError(Exception):
    """Exception raised for errors."""

    def __init__(self, message):
        """Class constructor."""
        super().__init__(message)
