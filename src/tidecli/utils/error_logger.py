"""Basic error handling and logging for the CLI application."""

__authors__ = ["Olli-Pekka Riikola, Olli Rutanen, Joni Sinokki"]
__license__ = "MIT"
__date__ = "11.5.2024"

import logging
import click
import os


class Logger:
    """Log different levels."""

    def __init__(self):
        """Class constructor."""
        # 10 is the lowest logging level, 50 highest, 0 means not set.
        TIDECLI_LOG_LEVEL = os.getenv("TIDECLI_LOG_LEVEL", 20)
        try:
            TIDECLI_LOG_LEVEL = int(TIDECLI_LOG_LEVEL)
        except Exception as e:
            TIDECLI_LOG_LEVEL = 50
            print(e)
            print('TIDECLI_LOG_LEVEL environment variable set incorrectly.')

        self.level = TIDECLI_LOG_LEVEL
        self.internal_logger = logging.getLogger(__name__)
        self.logfile = "tide-cli.log"
        logging.basicConfig(
            handlers=[
                logging.FileHandler(self.logfile, "a", "utf-8"),
                logging.StreamHandler(),
            ],
            level=self.level,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )

    def log(self, LEVEL, msg):
        """Log events with specified level."""
        self.internal_logger.log(LEVEL, msg)
        click.echo("Event was logged into {0}.".format(self.logfile))

    def debug(self, msg):
        """Log events with level DEBUG."""
        self.internal_logger.debug(msg)

    def info(self, msg):
        """Log events with level INFO."""
        self.internal_logger.info(msg)
