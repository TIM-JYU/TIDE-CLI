from pydantic import BaseModel


class TaskFile(BaseModel):
    """
    Model for single code file
    """
    code: str
    path: str


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