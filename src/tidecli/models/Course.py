from pydantic import BaseModel


class Course(BaseModel):
    """
    Course model
    """
    name: str
    id: int
    path: str
    task_paths: list[str]

    def pretty_print(self):
        task_paths = "\n".join(self.task_paths)
        return f"Course:\n{self.name}\nPath:\n{self.path}\nDemo paths:\n{task_paths}\n"
