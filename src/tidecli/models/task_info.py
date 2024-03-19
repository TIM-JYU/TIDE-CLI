from pydantic import BaseModel
from typing import Optional


class TaskInfo(BaseModel):
    header: str
    stem: str
    answer_count: Optional[int]
    type: str
