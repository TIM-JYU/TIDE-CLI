"""Basic error handling and logging for the CLI application."""

__authors__ = ["Olli-Pekka Riikola, Olli Rutanen, Joni Sinokki"]
__license__ = "MIT"
__date__ = "11.5.2024"

import logging
import click


class Logger:
    """Log different levels."""

    def __init__(self):
        """Class constructor."""

        # TODO: logging level via CLI-flag/env variable
        self.level = 30  # 10 is the lowest logging level, 50 highest, 0 means not set.
        self.internal_logger = logging.getLogger(__name__)
        self.logfile = "tide-cli.log"
        logging.basicConfig(
            handlers=[
                logging.FileHandler(self.logfile, "a", "utf-8"),
                logging.StreamHandler(),
            ],
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )

    def log(self, LEVEL, msg):

        # TODO: generic logger function with specified level
        self.internal_logger.log(LEVEL, msg)
        click.echo("Event was logged into {0}.".format(self.logfile))

    def debug(self, msg):
        """Log events with level DEBUG."""
        if self.level > logging.DEBUG:
            return
        self.internal_logger.debug(msg)

    def info(self, msg):
        """Log events with level INFO."""
        if self.level > logging.INFO:
            return
        self.internal_logger.info(msg)
