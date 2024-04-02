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
        """
        Prints the course as readable string.

        Return values with headings.
        :return: Course as string, like Course: <name>, ID: <id>
        """
        delimiter = "\n    - "
        task_paths = '{1}{0}'.format(delimiter.join(self.task_paths), delimiter)
        return f"Course: {self.name}, ID: {self.id}\n{task_paths} \n"
