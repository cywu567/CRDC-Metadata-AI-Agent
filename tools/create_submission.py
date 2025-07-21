from smolagents.tools import Tool
import os
import requests

class CreateSubmissionTool(Tool):
    name = "create_submission"
    description = "Creates a submission request in the data commons system."
    inputs = {
        "study_id": {"type": "string", "description": "The ID of the study to submit to."},
        "data_commons": {"type": "string", "description": "Name of the data commons (e.g., 'CDS')."},
        "name": {"type": "string", "description": "Unique submission name."},
        "intention": {"type": "string", "description": "Submission intention (e.g., 'New/Update')."},
        "data_type": {"type": "string", "description": "Type of submission (e.g., 'Metadata Only')."},
    }
    output_type = "object"

    def forward(self, study_id, data_commons, name, intention, data_type) -> dict:
        API_URL = "https://hub-qa.datacommons.cancer.gov/api/graphql"
        SUBMIT_TOKEN = os.getenv("SUBMITTER_TOKEN")

        headers = {
            "Authorization": f"Bearer {SUBMIT_TOKEN}",
            "Content-Type": "application/json"
        }

        mutation = """
        mutation createSubmission(
            $studyID: String!,
            $dataCommons: String!,
            $name: String!,
            $intention: String!,
            $dataType: String!
        ) {
            createSubmission(
                studyID: $studyID,
                dataCommons: $dataCommons,
                name: $name,
                intention: $intention,
                dataType: $dataType
            ) {
                _id
                status
                createdAt
            }
        }
        """

        variables = {
            "studyID": study_id,
            "dataCommons": data_commons,
            "name": name,
            "intention": intention,
            "dataType": data_type,
        }

        res = requests.post(API_URL, json={"query": mutation, "variables": variables}, headers=headers)

        if not res.ok:
            raise Exception(f"Error creating submission: {res.text}")
        data = res.json()
        if "errors" in data:
            raise Exception(f"GraphQL errors in create_submission: {data['errors']}")

        return data["data"]["createSubmission"]
