### **CRDC Metadata Submission Agent**

This project develops a custom AI agent to automate the end-to-end CRDC metadata submission workflow using the CRDC Datahub API. Built with modular Python tools handling tasks like retrieving studies, generating submission names, preparing metadata, and managing file uploads, the system is designed for cloud-native execution on AWS Bedrock. This eliminates local dependencies and enables scalable, reliable remote operation with all CRDC API interactions and file handling performed entirely in the cloud to ensure high availability and performance.

A key feature is an integrated feedback loop that collects system and user feedback, stores it in a vector database, and allows the agent to learn from execution outcomes and adapt over time, transforming it from a static script into an intelligent, self-improving assistant. The frontend user interface for interacting with the agent and visualizing feedback will be built using LangChain. The orchestration and multi-agent workflow management leverage the Smolagent framework to efficiently coordinate tasks and tools.



## Setup
1. **Activate the Python virtual environment:**

   ```bash
   source .venv/bin/activate
   ```

2. **Add Your CRDC  submission token in your shell**
```bash
   export SUBMITTER_TOKEN=your_api_token
```

3. **Install requirements**
   ```bash
   pip install os, smolagent, requests
   ```

4. To run,

```bash
python CustomAgent_Smolagent.py
```    
