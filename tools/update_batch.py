from smolagents.tools import Tool
import requests
import os

class UpdateBatchTool(Tool):
    name = "update_batch"
    description = "Updates the batch after file uploads with required UploadResult fields."
    inputs = {"batch_id": {"type": "string","description": "The ID of the batch to update."},
            "file_names": {"type": "array","description": "List of uploaded file names to mark as succeeded."}
    }
    output_type = "object"

    def forward(self, batch_id, file_names) -> dict:
        API_URL = "https://hub-qa.datacommons.cancer.gov/api/graphql"
        SUBMIT_TOKEN = os.getenv("SUBMITTER_TOKEN")

        headers = {
            "Authorization": f"Bearer {SUBMIT_TOKEN}",
            "Content-Type": "application/json"
        }

        mutation = """
        mutation updateBatch($batchID: ID!, $files: [UploadResult]!) {
          updateBatch(batchID: $batchID, files: $files) {
            _id
            submissionID
            type
            fileCount
            files {
              filePrefix
              fileName
              size
              status
              errors
              createdAt
              updatedAt
            }
            status
            createdAt
            updatedAt
          }
        }
        """

        files_payload = [{"fileName": f, "succeeded": True, "errors": None} for f in file_names]

        variables = {
            "batchID": batch_id,
            "files": files_payload
        }

        res = requests.post(API_URL, json={"query": mutation, "variables": variables}, headers=headers)
        if not res.ok:
            raise Exception(f"Error updating batch: {res.text}")
        data = res.json()
        if "errors" in data:
            raise Exception(f"GraphQL errors: {data['errors']}")

        return data["data"]["updateBatch"]