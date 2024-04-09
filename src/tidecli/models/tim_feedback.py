from pydantic import BaseModel


class WebData(BaseModel):
    console: str | None = None
    error: str
    language: str | None = None
    pwd: str | None = None
    runtime: str | None = None


class TimFeedback(BaseModel):
    """
    Model for feedback response after submitting a task
    """

    savedNew: int | None
    valid: bool
    web: WebData | None

    def console_output(self):
        """
        Returns the console output of the task
        """

        if self.web.error != "":
            return self.web.error

        if self.savedNew:
            saved_new = "Saved new answer successfully."
        else:
            saved_new = "New answer was not saved. Same file was already submitted."

        return f"{saved_new}\n\nStats for nerds:\n{self.web.runtime}\nConsole feedback:\n{self.web.console}"
