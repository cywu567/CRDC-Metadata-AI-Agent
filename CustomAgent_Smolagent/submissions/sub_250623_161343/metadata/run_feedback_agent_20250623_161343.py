from db.db import init_schema
from smolagents.agents import CodeAgent
from smolagents.models import AmazonBedrockServerModel
from tools.generate_submission_name import GenerateSubmissionNameTool
from tools.prepare_metadata        import PrepareAllMetadataTool
from tools.get_my_studies          import GetMyStudiesTool
from tools.create_submission       import CreateSubmissionTool
from tools.create_batch            import CreateBatchTool
from tools.log_feedback            import LogFeedbackTool
from feedback_input import ask_user_feedback

init_schema()   # create tables if first run

model = AmazonBedrockServerModel(
    model_id="anthropic.claude-3-haiku-20240307-v1:0",
    client_kwargs={"region_name":"us-east-1"},
    inferenceConfig={"maxTokens":2048}
)

agent = CodeAgent(
    tools=[
        GenerateSubmissionNameTool(),
        PrepareAllMetadataTool(),
        GetMyStudiesTool(),
        CreateSubmissionTool(),
        CreateBatchTool(),
        LogFeedbackTool(),
    ],
    max_steps = 5,
    model = model
)

feedback_logger = LogFeedbackTool()

PROMPT_HEADER = """
You are a Python REPL.  
**Reply ONLY in this schema** — nothing before or after it:

Thoughts:
<concise reasoning here — one or two lines max>

Code:
```python
# your python code here
'''
<end_code>

Done
"""

STEPS = [
    # 1 – submission name
    "Generate a unique submission name with generate_submission_name(), "
    "store it in variable submission_name, and print submission_name.",

    # 2 – metadata
    "Use PrepareAllMetadataTool for the inputs in '/Users/celinewu/Desktop/ESI 2025/CRDC/inject3_metadata_batch2/', "
    "and have the base_directory be '/Users/celinewu/Desktop/ESI 2025/CRDC/CustomAgent_Smolagent'). "
    "Save the returned list in variable metadata and print metadata.",

    # 3 – extract file info
    "From metadata, build two lists: file_names (each element's 'fileName') and full_paths (each 'fullPath'). "
    "Print file_names.",

    # 4 – latest study
    "Get the user's studies with get_my_studies() and assign the first element to study_id. "
    "Print study_id.",

    # 5 – create submission
    "Create a submission by calling create_submission(study_id, 'CDS', submission_name, 'New/Update', 'Metadata Only'). "
    "Save the returned _id to submission_id and print submission_id.",
]

STEP_PROMPTS = [PROMPT_HEADER + "\n\nTask:\n" + body for body in STEPS]

def main() -> None:
    print("\n--- Running Feedback Agent ---")
    for idx, prompt in enumerate(STEP_PROMPTS, start=1):
        try:
            result       = agent.run(prompt)
            system_ok    = True
            system_note  = "Step executed without exceptions."
        except Exception as err:
            result       = f"Exception: {err}"
            system_ok    = False
            system_note  = str(err)

        print(f"\nOutput of Step {idx}:\n{result}")
        
        try:
            feedback_logger.forward(
                file_id     = idx,
                source      = "system",
                is_accepted = system_ok,
                comments    = system_note,
            )
        except Exception as e:
            print(f"DB write failed for system feedback on step{idx}: {e}")


        #accepted_raw, comment = ask_user_feedback(idx, prompt)
        #accepted = accepted_raw.lower().startswith("y")

        ## record feedback (step index used as placeholder file_id)
        #try:
        #    feedback_logger.forward(
        #        file_id     = idx,
        #        source      = "user",
        #        is_accepted = accepted,
        #        comments    = comment,
        #    )
        #except Exception as e:
        #    print(f"DB write failed for user feedback on step{idx}: {e}")

    print("\n✓ All steps complete. Feedback stored in feedback.db")

if __name__ == "__main__":
    main()
