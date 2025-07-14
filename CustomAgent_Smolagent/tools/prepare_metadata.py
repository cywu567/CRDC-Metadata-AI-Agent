from smolagents.tools import Tool
from typing import List, Dict
from typing import Type
from pydantic import BaseModel, Field
#from db.db import log_feedback, get_file_id, insert_file, get_feedback_for_tool
from datetime import datetime
import time
import os
import shutil


class PrepareAllMetadataTool(Tool):
    name = "prepare_all_metadata"
    description = (
        "Copies all files from the specified folder into a new submission metadata folder, "
        "renames each file with a timestamp, and returns metadata for each copied file."
    )
    inputs = {
        "folder_path": {"type": "string","description": "Path to the folder containing raw metadata files."},
        "base_dir": {"type": "string","description": "Base directory where the 'submissions' folder will be created."},
        "submission_name": {"type": "string","description": "Unique name used to create the metadata submission subfolder."}
    }
    output_type = "array"

    def forward(self, folder_path: str, base_dir: str, submission_name: str) -> list[dict]:
        # Determine where to put submissions
        if os.path.basename(base_dir) == "submissions":
            submissions_root = base_dir
        elif os.path.basename(base_dir) == "CustomAgent-Smolagent":
            submissions_root = os.path.join(base_dir, "submissions")
        else:
            submissions_root = os.path.join(base_dir, "CustomAgent_Smolagent", "submissions")
        os.makedirs(submissions_root, exist_ok=True)

        # Create folders
        submission_folder = os.path.join(submissions_root, submission_name)
        os.makedirs(submission_folder, exist_ok=True)

        metadata_folder = os.path.join(submission_folder, "metadata")
        os.makedirs(metadata_folder, exist_ok=True)

        results = []
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                base_name, ext = os.path.splitext(filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                new_file_name = f"{base_name}_{timestamp}{ext}"
                dest_path = os.path.join(metadata_folder, new_file_name)
                shutil.copy(file_path, dest_path)
                results.append({
                    "submission_folder": submission_folder,
                    "metadata_folder": metadata_folder,
                    "updated_file_path": dest_path,
                    "fileName": new_file_name,
                    "fullPath": dest_path,
                    "submission_id": f"{submission_name}_{int(time.time())}",
                    "created_at": datetime.now().isoformat(),
                })

        return results