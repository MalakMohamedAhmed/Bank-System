import os
import subprocess

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO  = os.environ.get("GITHUB_REPO")

def setup_git():
    """Configure git identity and remote with token — run once on startup."""
    remote_url = f"https://x-access-token:{GITHUB_TOKEN}@github.com/{GITHUB_REPO}.git"
    subprocess.run(["git", "config", "user.email", "bot@nexabank.com"], check=True)
    subprocess.run(["git", "config", "user.name",  "NexaBank Bot"],     check=True)
    subprocess.run(["git", "remote", "set-url", "origin", remote_url],  check=True)

def pull():
    """Pull latest data files from GitHub before reading."""
    subprocess.run(["git", "pull", "origin", "main"], check=True)

def push(message="update data"):
    """Stage CSVs and push to GitHub after every write."""
    subprocess.run(["git", "add", "bank_data.csv", "transactions.csv"], check=True)
    result = subprocess.run(["git", "diff", "--cached", "--quiet"])
    if result.returncode == 0:
        return  # nothing changed, skip push
    subprocess.run(["git", "commit", "-m", message], check=True)
    subprocess.run(["git", "push", "origin", "main"],  check=True)
