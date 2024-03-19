from pydantic import BaseModel


class Course(BaseModel):
    """
    Course model
    """
    name: str
    id: int
    path: str
    demo_paths: list[str]

    def pretty_print(self):
        demos = "\n".join(self.demo_paths)
        return f"Course:\n{self.name}\nPath:\n{self.path}\nDemo paths:\n{demos}\n"
