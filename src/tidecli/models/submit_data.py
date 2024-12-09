"""
Validates and formats the data for submitting a task.

Functions are used by main program and utility functions.
"""

__authors__ = ["Olli-Pekka Riikola, Olli Rutanen, Joni Sinokki"]
__license__ = "MIT"
__date__ = "11.5.2024"

from pydantic import BaseModel

from tidecli.models.task_data import TaskFile


class SubmitData(BaseModel):
    """Model for submittable task."""

    code_files: TaskFile | list[TaskFile]
    code_language: str  # Plugin "type"

    def submit_json(self) -> dict:
        """Print the course as readable JSON string."""
        if isinstance(self.code_files, TaskFile):
            self.code_files = [self.code_files]

        return {
            "code_files": [file.to_json() for file in self.code_files],
            "code_language": self.code_language,
        }
