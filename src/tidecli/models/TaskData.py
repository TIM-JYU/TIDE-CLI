from pydantic import BaseModel


class TaskFile(BaseModel):
    """Model for single code file."""

    content: str
    file_name: str = ""
    source: str = "editor"
    user_input: str | None = ""
    user_args: str | None = ""
    task_id: str

    def to_json(self):
        """Convert to JSON."""
        return {
            "task_id": self.task_id,
            "content": self.content,
            "file_name": self.file_name,
            "source": self.source,
            "user_input": self.user_input,
            "user_args": self.user_args,
        }


class TaskData(BaseModel):
    """Model for task data."""

    header: str | None = None
    stem: str | None = None
    type: str
    doc_id: int
    ide_task_id: str
    task_files: list[TaskFile]

    def pretty_print(self):
        """
        Pretty print the task data.

        Prints the task data in a readable string.
        :return: Task data as string like Task: <header>, ID: <ide_task_id>

        """
        if self.header is not None:
            return f"Taskname: {self.header}, ID: {self.ide_task_id}"
        else:
            return f"ID: {self.ide_task_id}"
