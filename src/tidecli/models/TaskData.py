from pydantic import BaseModel


class TaskFile(BaseModel):
    """Model for single code file."""

    content: str
    filename: str = None
    source: str = "editor"

    def to_json(self):
        """Convert to JSON."""
        return {
            "content": self.content,
            "path": self.filename,
            "source": self.source
        }


class TaskData(BaseModel):
    """Model for task data."""

    header: str | None = None
    stem: str | None = None
    type: str
    task_id: str
    par_id: str
    doc_id: int
    ide_task_id: str
    task_files: list[TaskFile]

    def pretty_print(self):
        """
        Pretty print the task data.

        Prints the task data in a readable string.
        :return: Task data as string like Task: <header>, ID: <ide_task_id>

        """
        return f"Taskname: {self.header}, ID: {self.ide_task_id}"
