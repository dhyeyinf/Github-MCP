# pull_request_ops.py
from github import Github
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("GITHUB_TOKEN")
g = Github(token)

def create_pull_request(repo_name, base_branch, head_branch, title, body=""):
    """
    Create a pull request from head_branch into base_branch
    """
    try:
        repo = g.get_repo(repo_name)
        pr = repo.create_pull(
            title=title,
            body=body,
            head=head_branch,
            base=base_branch
        )
        return f"✅ Pull request created: {pr.html_url}"
    except Exception as e:
        return f"[ERROR] Could not create PR: {str(e)}"
