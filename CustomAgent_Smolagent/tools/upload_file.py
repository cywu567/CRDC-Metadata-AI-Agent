from smolagents.tools import Tool
from pydantic import BaseModel, Field
import mimetypes
#from db.db import log_feedback, get_file_id
import requests

class UploadFileTool(Tool):
    name = "upload_file"
    description = (
        "Extracts the signed URL for a specific file name from the batch object and uploads a local file to it via HTTP PUT."
    )
    inputs = {
        "batch": {"type": "object", "description": "The batch object returned from create_batch."},
        "file_name": {"type": "string", "description": "The name of the file to upload."},
        "file_path": {"type": "string", "description": "Local file path to be uploaded."}
    }
    output_type = "string"

    def forward(self, batch, file_name, file_path) -> str:
        presigned_url = None
        for file_info in batch["files"]:
            if file_info["fileName"] == file_name:
                presigned_url = file_info["signedURL"]
                break

        if presigned_url is None:
            raise ValueError(f"File '{file_name}' not found in batch.")

        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = "application/octet-stream"

        headers = {
            "Content-Type": mime_type
        }

        with open(file_path, "rb") as f:
            file_data = f.read()

        res = requests.put(presigned_url, data=file_data, headers=headers)
        if not res.ok:
            raise Exception(f"Error uploading file {file_path}: {res.text}")

        return f"Uploaded {file_path}"