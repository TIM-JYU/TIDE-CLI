from pydantic import BaseModel


class CourseTask(BaseModel):
    """
    CourseTask model
    """

    name: str
    doc_id: int
    path: str


class Course(BaseModel):
    """
    Course model
    """

    name: str
    id: int
    path: str
    tasks: list[CourseTask]

    def pretty_print(self):
        """
        Prints the course as readable string.

        Return values with headings.
        :return: Course as string, like Course: <name>, ID: <id>
        """
        delimiter = "    - "
        task_paths = [
            f"{delimiter}{task.name}, ID: {task.doc_id}, Path: {task.path}\n"
            for task in self.tasks
        ]

        return f"Course: {self.name}, ID: {self.id}\n{''.join(task_paths)}"
