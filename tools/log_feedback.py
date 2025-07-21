from smolagents.tools import Tool
from pydantic import BaseModel, Field
from typing import Literal
from db.db import log_feedback

class FeedbackInput(BaseModel):
    file_id: int = Field(..., description="Row ID in `files` (or step index)")
    tool_name: str = Field(..., description="Name of the tool providing feedback.")
    source: Literal["user", "system"] = Field(..., description="'user' or 'system'")
    is_accepted: bool = Field(..., description="True for YES, False for NO")
    comments: str = Field(..., description="Optional free-text")

class LogFeedbackTool(Tool):
    name        = "log_feedback"
    description = "Persist feedback (yes/no + comment) into feedback.db"
    input_model  = FeedbackInput
    output_type = "string"
    inputs = input_model.model_json_schema()["properties"]

    def forward(self, file_id: int, tool_name: str, source: str, is_accepted: bool, comments: str) -> str:
        log_feedback(
            file_id=file_id,
            tool_name=tool_name,
            source=source,
            is_accepted=is_accepted,
            comments=comments,
        )
        return "Feedback recorded."
