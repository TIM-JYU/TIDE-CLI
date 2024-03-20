from pydantic import BaseModel


class TaskFile(BaseModel):
    """
    Model for single code file
    """
    content: str
    path: str
    source: str = "editor"

    def to_json(self):
        return {
            "content": self.content,
            "path": self.path,
            "source": self.source
        }


class TaskData(BaseModel):
    """
    Model for task data
    """
    header: str | None = None
    stem: str | None = None
    type: str
    task_id: str
    par_id: str
    doc_id: int
    ide_task_id: str
    task_files: list[TaskFile]