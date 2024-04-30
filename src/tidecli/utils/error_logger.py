import logging
import time
import click
from functools import wraps

# ODO: vaihda lokittaja käyttämään muuta kuin baseloggeria
# Configure logger
logging.basicConfig(
    filename="tide-cli.log",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def error_handler(func):
    """
    Generic error handler

    This is used as decorator @error_handler
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Log the error
            logging.error(f"Error in function {func.__name__}: {e}")
            # You can add more actions here, like sending an email notification or printing the error to console
            # For simplicity, I'm just re-raising the error here
            # raise
            print("\033[91m {}\033[00m".format(e))

    return wrapper


logger = logging.getLogger(__name__)

# Misc logger setup so a debug log statement gets printed on stdout.
logger.setLevel("ERROR")
handler = logging.StreamHandler()
log_format = "%(asctime)s %(levelname)s -- %(message)s"
formatter = logging.Formatter(log_format)
handler.setFormatter(formatter)
logger.addHandler(handler)


def timed(func):
    """Print the execution time for the decorated function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logging.info("{} ran in {}s".format(func.__name__, round(end - start, 2)))
        return result

    return wrapper


# TODO: Add error handling for specific errors
class CliError(Exception):
    """
    Exception raised for errors
    """

    def __init__(self, message):
        super().__init__(message)
