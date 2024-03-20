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
            return self.web.console + "\n" + "Saved answer number: " + str(self.savedNew)
        else:
            return "Answer was the same as the previous one."
