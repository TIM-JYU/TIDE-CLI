from pydantic import BaseModel


class SubmitData(BaseModel):
    """
    Model for submittable task
    """
    code_files: str | list[str]
    path: str
    task_id: str
    doc_id: int

    def submit_json(self):
        if isinstance(self.code_files, str):
            self.code_files = [self.code_files]

        return {
            "code_files": self.code_files,
            "task_id_ext": str(self.doc_id) + "." + self.task_id  # "<doc_id>.<task_id>"
        }
