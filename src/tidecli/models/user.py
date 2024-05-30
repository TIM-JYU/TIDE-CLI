
"""
Datamodel for user.

Provides helper class for keyring save.
"""
from dataclasses import dataclass

__authors__ = ["Olli-Pekka Riikola, Olli Rutanen, Joni Sinokki"]
__license__ = "MIT"
__date__ = "11.5.2024"


@dataclass
class User:
    """Dataclass for user."""

    username: str
    password: str
