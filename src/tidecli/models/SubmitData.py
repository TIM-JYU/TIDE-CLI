from pydantic import BaseModel

from tidecli.models.TaskData import TaskFile


class SubmitData(BaseModel):
    """
    Model for submittable task
    """
    code_files: TaskFile | list[TaskFile]
    task_id: str
    doc_id: int
    code_language: str  # Plugin "type"

    def submit_json(self):
        if isinstance(self.code_files, TaskFile):
            self.code_files = [self.code_files]
        return {
            "code_files": [file.to_json() for file in self.code_files],
            "code_language": self.code_language,
            "task_id_ext": str(self.doc_id) + "." + self.task_id  # "<doc_id>.<task_id>"
        }
