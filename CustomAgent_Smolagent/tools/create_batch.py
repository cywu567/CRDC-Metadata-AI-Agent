from smolagents.tools import Tool
#from db.db import log_feedback, get_file_id
from typing import Type
from pydantic import BaseModel, Field
import os
import requests

API_URL = "https://hub-qa.datacommons.cancer.gov/api/graphql"
SUBMIT_TOKEN = os.getenv("SUBMITTER_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {SUBMIT_TOKEN}",
    "Content-Type": "application/json"
}


class CreateBatchTool(Tool):
    name = "create_batch"
    description = (
        "Creates a batch in the submission to group files for upload, returning presigned URLs."
    )
    inputs = {
        "submission_id": {"type": "string", "description": "ID of the submission"},
        "file_names": {"type": "string", "description": "List of filenames to include"},
        "batch_type": {"type": "string", "description": "Type of batch (default: metadata)"}
    }
    output_type = "object"

    def forward(self, submission_id, file_names, batch_type) -> dict:

        mutation = """
        mutation createBatch($submissionID: ID!, $type: String, $files: [String!]!) {
          createBatch(submissionID: $submissionID, type: $type, files: $files) {
            _id
            submissionID
            bucketName
            filePrefix
            type
            fileCount
            files {
              fileName
              signedURL
            }
            status
            createdAt
            updatedAt
          }
        }
        """

        variables = {
            "submissionID": submission_id,
            "type": batch_type,
            "files": file_names,
        }

        res = requests.post(API_URL, json={"query": mutation, "variables": variables}, headers=HEADERS)

        if not res.ok:
            raise Exception(f"Error creating batch: {res.text}")
        data = res.json()
        if "errors" in data:
            raise Exception(f"GraphQL errors: {data['errors']}")

        return data["data"]["createBatch"]