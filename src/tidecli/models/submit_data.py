from pydantic import BaseModel

from tidecli.models.task_data import TaskFile


class SubmitData(BaseModel):
    """
    Model for submittable task
    """

    code_files: TaskFile | list[TaskFile]
    code_language: str  # Plugin "type"

    def submit_json(self):
        if isinstance(self.code_files, TaskFile):
            self.code_files = [self.code_files]
        return {
            "code_files": [file.to_json() for file in self.code_files],
            "code_language": self.code_language,
        }
