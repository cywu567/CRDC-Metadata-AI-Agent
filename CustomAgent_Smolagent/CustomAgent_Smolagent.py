from smolagents import CodeAgent
from tools.generate_submission_name import GenerateSubmissionNameTool
from tools.prepare_metadata import PrepareAllMetadataTool
from tools.get_my_studies import GetMyStudiesTool
from tools.create_submission import CreateSubmissionTool
from tools.create_batch import CreateBatchTool
from tools.update_batch import UpdateBatchTool
#from tools.log_feedback import LogFeedbackTool
from tools.upload_file import UploadFileTool
from smolagents.models import AmazonBedrockServerModel
#from db import init_schema

#init_schema()

agent = CodeAgent(tools=[
        GenerateSubmissionNameTool(),
        PrepareAllMetadataTool(),
        GetMyStudiesTool(),
        CreateSubmissionTool(),
        CreateBatchTool(),
        UpdateBatchTool(),
        #LogFeedbackTool(),
        UploadFileTool()
    ],
        model = AmazonBedrockServerModel(
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
        )
    )

# Determine latest study ID just once
latest_study = GetMyStudiesTool().forward()[0]


prompt = f"""
You are an agent executing the following steps to prepare and upload metadata files to the CRDC submission system.

For each step, think about what you are doing and then respond in the following format:
Thoughts: Your thoughts about the step
Code:
```py
# Your Python code here

Next for the actual prompt:
"Call generate_submission_name() and save the result as `submission_name`.",

    "Call prepare_all_metadata() with:
        folder_path='/Users/celinewu/Desktop/ESI 2025/CRDC/inject3_metadata_batch2/',
        base_dir='/Users/celinewu/Desktop/ESI 2025/CRDC/CustomAgent_Smolagent/submissions',
        submission_name=submission_name.
     Save the result as `metadata_files`.",

    "Assign the latest study ID '{latest_study}' to `study_id`.",

    "Call create_submission(name=submission_name, study_id=study_id,
                            data_commons='CDS', intention='New/Update', data_type='Metadata Only')
     and save the `_id` as `submission_id`.",

    "Extract the 'fileName' field from each item in metadata_files.
     Then call create_batch(submission_id=submission_id, file_names=file_names, submission_name=submission_name),
     and save the returned object as `batch`. Also extract and store `batch_id = batch['_id']`.",

    "For each item in metadata_files, call:
        upload_file(batch=batch, file_name=item['fileName'], file_path=item['fullPath']).
     Save all confirmation strings as `upload_results`.",

    "Finally, call update_batch(batch_id=batch_id, file_names=file_names) to finalize the batch."

"""


# Run once with a full task list
result = agent.run(prompt)
print("\nFinal Output:\n", result)
