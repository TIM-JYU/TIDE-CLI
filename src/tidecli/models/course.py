from typing import Any

from pydantic import BaseModel


class CourseTask(BaseModel):
    """
    CourseTask model
    """

    name: str
    doc_id: int
    path: str


class Course(BaseModel):
    """
    Course model
    """

    name: str
    id: int
    path: str
    tasks: list[CourseTask]

    def pretty_print(self) -> str:
        """
        Prints the course as readable string.

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
        Converts the course to JSON.

        :return: Course as JSON
        """
        return {
            "name": self.name,
            "id": self.id,
            "path": self.path,
            "task_docs": [task.dict() for task in self.tasks],
        }
