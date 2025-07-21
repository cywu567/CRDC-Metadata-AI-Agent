from smolagents.tools import Tool
from pydantic import BaseModel, Field
from typing import Literal
from db.db import get_feedback_for_file


class NavigateInput(BaseModel):
    file_name: str = Field(..., description="The file the tool was applied to.")
    tool_name: str = Field(..., description="The tool used on this file.")

class NavigateTool(Tool):
    name = "navigate"
    description = (
        "Check if a tool should be skipped, repeated, or modified based on past feedback."
    )
    input_model = NavigateInput
    output_type = "string"
    inputs = input_model.model_json_schema()["properties"]

    def forward(self, file_name: str, tool_name: str) -> str:
        feedback = get_feedback_for_file(file_name, tool_name)

        if not feedback:
            return "proceed"  # No prior feedback, run as usual

        if feedback["accepted"]:
            return "skip"

        if feedback["comments"]:
            return f"repeat: {feedback['comments']}"

        return "repeat"
