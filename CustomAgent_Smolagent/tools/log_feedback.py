#"""
#tools/log_feedback.py
#Smolagent Tool that records a yes/no + comment row in feedback.db.
#"""

#from pydantic import BaseModel, Field
#from typing import Literal
#from db import log_feedback

#class FeedbackInput(BaseModel):
#    file_id: int = Field(..., description="Row ID in `files` (or step index)")
#    source: Literal["user", "system"] = Field(..., description="'user' or 'system'")
#    is_accepted: bool = Field(..., description="True for YES, False for NO")
#    comments: str = Field(..., description="Optional free-text")

#class LogFeedbackTool(Tool):
#    name        = "log_feedback"
#    description = "Persist feedback (yes/no + comment) into feedback.db"
#    input_type  = FeedbackInput
#    output_type = str

#    def forward(self, args: FeedbackInput) -> str:
#        log_feedback(
#            file_id     = args.file_id,
#            source      = args.source,
#            is_accepted = args.is_accepted,
#            comments    = args.comments,
#        )
#        return "Feedback recorded."
