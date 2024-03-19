from pydantic import BaseModel
from tidecli.models.ide_files import IdeFiles
from tidecli.models.task_info import TaskInfo


class AllData(BaseModel):
    ide_files: IdeFiles
    task_info: TaskInfo
    task_id: str
    document_id: int
    paragraph_id: str
    ide_task_id: str

    def to_json(self):
        return {
            "ide_files": self.ide_files.dict(),
            "task_info": self.task_info.dict(),
            "task_id": self.task_id,
            "document_id": self.document_id,
            "paragraph_id": self.paragraph_id,
            "ide_task_id": self.ide_task_id,
        }
