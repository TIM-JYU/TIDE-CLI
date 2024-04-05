import re

from pydantic import BaseModel


class TaskFile(BaseModel):
    """Model for single code file."""

    task_id_ext: str
    content: str
    file_name: str = ""
    source: str = "editor"
    user_input: str = ""
    user_args: str = ""

    def to_json(self):
        """Convert to JSON."""
        return {
            "task_id_ext": self.task_id_ext,
            "content": self.content,
            "file_name": self.file_name,
            "source": self.source,
            "user_input": self.user_input,
            "user_args": self.user_args,
        }


_task_type_split_re = re.compile(r"[/,; ]")


class TaskData(BaseModel):
    """Model for task data."""

    path: str
    type: str
    doc_id: int
    ide_task_id: str
    task_files: list[TaskFile]
    stem: str | None = None
    header: str | None = None

    @property
    def run_type(self) -> str:
        """Returns run type eg. cc from cc/input/comtest"""
        return _task_type_split_re.split(self.type)[0]

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
