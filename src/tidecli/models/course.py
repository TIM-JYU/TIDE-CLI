"""
This module contains the Course and CourseTask models.

Models are used to validate data from TIM API.
"""

authors = ["Olli-Pekka Riikola, Olli Rutanen, Joni Sinokki"]
license = "MIT"
date = "11.5.2024"

from typing import Any

from pydantic import BaseModel


class CourseTask(BaseModel):
    """Simple model for course task."""

    name: str
    """Task name."""

    doc_id: int
    """Doc ID, where task/csPlugin belongs to."""

    path: str
    """Task virtual path in TIM."""


class Course(BaseModel):
    """Course model."""

    name: str
    """Course name."""

    id: int
    """Course ID."""

    path: str
    """Course virtual path in TIM."""

    tasks: list[CourseTask]
    """List of tasks in the course defined in TIM."""

    def pretty_print(self) -> str:
        """
        Print the course as readable string.

        Return values with headings.
        :return: Course as string, like Course: <name>, ID: <id>
        """
        delimiter = "    - "
        task_paths = [
            f"{delimiter}{task.name}, ID: {task.doc_id}, Path: {task.path}\n"
            for task in self.tasks
        ]

        return f"Course: {self.name}, ID: {self.id}\n{''.join(task_paths)}"

    def to_json(self) -> dict[str, Any]:
        """
        Convert the course to JSON.

        :return: Course as JSON
        """
        return {
            "name": self.name,
            "id": self.id,
            "path": self.path,
            "task_docs": [task.dict() for task in self.tasks],
        }
