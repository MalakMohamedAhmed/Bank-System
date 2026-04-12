import os
from huggingface_hub import HfApi, hf_hub_download

HF_TOKEN   = os.environ.get("HF_TOKEN")
DATASET_ID = "your-username/nexabank-data"  # change this

api = HfApi()

def pull():
    """Download CSVs from HF dataset to local filesystem."""
    for filename in ["bank_data.csv", "transactions.csv"]:
        try:
            path = hf_hub_download(
                repo_id=DATASET_ID,
                filename=filename,
                repo_type="dataset",
                token=HF_TOKEN,
                local_dir="."
            )
        except Exception:
            pass  # file doesn't exist yet, will be created on first write

def push(message="update data"):
    """Upload CSVs to HF dataset after every write."""
    for filename in ["bank_data.csv", "transactions.csv"]:
        if os.path.exists(filename):
            api.upload_file(
                path_or_fileobj=filename,
                path_in_repo=filename,
                repo_id=DATASET_ID,
                repo_type="dataset",
                token=HF_TOKEN,
                commit_message=message
            )
