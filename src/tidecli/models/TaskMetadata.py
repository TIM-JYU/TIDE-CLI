"""Model for task metadata."""

import json
from pydantic import BaseModel


class TaskMetadata(BaseModel):
    """
    Model for task metadata.

    This is provided a along with taskfiles.
    """

    task_id: str
    demo_path: str
    doc_id: int
    code_language: str

    def to_json(self):
        """Convert to JSON."""
        return {
            "task_id": self.task_id,
            "demo_path": self.demo_path,
            "doc_id": self.doc_id,
            "code_language": self.code_language
        }

    def pretty_print(self):
        """
        Pretty print the metadata.

        Prints the metadata in a readable format as JSON string.
        """
        return json.dumps(self.to_json(), indent=4, ensure_ascii=False)
