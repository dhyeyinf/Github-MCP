# issues_client.py

from github import Github
from dotenv import load_dotenv
import os
load_dotenv()
token = os.getenv("GITHUB_TOKEN")
g = Github(token)

def list_issues(repo_name, state="open"):
    """List issues in a repository (open or closed)"""
    try:
        repo = g.get_repo(repo_name)
        issues = repo.get_issues(state=state)
        issue_list = []
        for issue in issues:
            if issue.pull_request is None:  # Ignore PRs
                issue_list.append({
                    "number": issue.number,
                    "title": issue.title,
                    "creator": issue.user.login,
                    "created_at": issue.created_at.strftime('%Y-%m-%d %H:%M')
                })
        return issue_list
    except Exception as e:
        return f"[ERROR] Failed to list issues: {str(e)}"

def list_issue_comments(repo_name, issue_number):
    """Get all comments on a specific issue"""
    try:
        repo = g.get_repo(repo_name)
        issue = repo.get_issue(number=issue_number)
        comments = issue.get_comments()
        return [{
            "user": comment.user.login,
            "created_at": comment.created_at.strftime('%Y-%m-%d %H:%M'),
            "body": comment.body
        } for comment in comments]
    except Exception as e:
        return f"[ERROR] Could not fetch comments: {str(e)}"

def add_issue_comment(repo_name, issue_number, comment_body):
    """Add a comment to a specific issue"""
    try:
        repo = g.get_repo(repo_name)
        issue = repo.get_issue(number=issue_number)
        issue.create_comment(comment_body)
        return "✅ Comment added successfully."
    except Exception as e:
        return f"[ERROR] Failed to add comment: {str(e)}"

def create_issue(repo_name, title, body=""):
    """Create a new issue in the specified repository"""
    try:
        repo = g.get_repo(repo_name)
        issue = repo.create_issue(title=title, body=body)
        return {
            "message": f"✅ Issue #{issue.number} created successfully.",
            "number": issue.number,
            "title": issue.title,
            "created_at": issue.created_at.strftime('%Y-%m-%d %H:%M')
        }
    except Exception as e:
        return {"error": f"[ERROR] Failed to create issue: {str(e)}"}
