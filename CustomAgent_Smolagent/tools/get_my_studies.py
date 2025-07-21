from smolagents.tools import Tool
import requests
import os

class GetMyStudiesTool(Tool):
    name = "get_my_studies"
    description = "Fetches study IDs for the user using the CRDC GraphQL API."
    inputs = {}
    output_type = "array"

    def forward(self) -> list[str]:
        API_URL = "https://hub-qa.datacommons.cancer.gov/api/graphql"
        SUBMIT_TOKEN = os.getenv("SUBMITTER_TOKEN")

        headers = {
            "Authorization": f"Bearer {SUBMIT_TOKEN}",
            "Content-Type": "application/json"
        }

        query = """
        query getMyUser {
          getMyUser {
            _id
            studies {
              _id
            }
          }
        }
        """

        res = requests.post(API_URL, json={"query": query}, headers=headers)
        if not res.ok:
            raise Exception(f"Error fetching studies: {res.text}")
        data = res.json()

        return [s["_id"] for s in data["data"]["getMyUser"]["studies"]]
