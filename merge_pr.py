# merge_pr.py
from github import Github
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("GITHUB_TOKEN")
g = Github(token)

def merge_pull_request(repo_name, pr_number, merge_message="Merging via script"):
    """
    Merge the given PR by number
    """
    try:
        repo = g.get_repo(repo_name)
        pr = repo.get_pull(pr_number)
        if pr.is_merged():
            return f"⚠️ PR #{pr_number} is already merged."

        if not pr.mergeable:
            return f"❌ PR #{pr_number} is not mergeable right now."

        pr.merge(commit_message=merge_message)
        return f"✅ Merged PR #{pr_number} successfully!"
    except Exception as e:
        return f"[ERROR] Could not merge PR #{pr_number}: {str(e)}"
