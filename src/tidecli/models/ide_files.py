from pydantic import BaseModel


class IdeFiles(BaseModel):
    code: str
    path: str
