
"""
Datamodel for user.

Provides helper class for keyring save.
"""
from dataclasses import dataclass

authors = ["Olli-Pekka Riikola, Olli Rutanen, Joni Sinokki"]
license = "MIT"
date = "11.5.2024"


@dataclass
class User:
    """Dataclass for user."""

    username: str
    password: str
