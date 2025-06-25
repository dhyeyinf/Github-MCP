# review_pr.py

from github import Github
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("GITHUB_TOKEN")
g = Github(token)

def comment_on_pull_request(repo_name, pr_number, comment_body):
    """
    Add a general comment to a pull request
    """
    try:
        repo = g.get_repo(repo_name)
        pr = repo.get_pull(pr_number)
        pr.create_issue_comment(comment_body)
        return f"✅ Comment added to PR #{pr_number}"
    except Exception as e:
        return f"[ERROR] Could not comment on PR #{pr_number}: {str(e)}"
