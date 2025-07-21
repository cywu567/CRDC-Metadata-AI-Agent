from smolagents.tools import Tool
from datetime import datetime

class GenerateSubmissionNameTool(Tool):
    name = "generate_submission_name"
    description = (
        "Generate a unique submission name starting with 'sub_' followed by the current date and time "
        "in the format YYMMDD_HHMMSS. This ensures the name is unique and under 25 characters."
    )
    inputs = {}
    output_type = "string"

    def forward(self) -> str:
        return "sub_" + datetime.now().strftime("%y%m%d_%H%M%S")
