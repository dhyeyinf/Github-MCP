# repo_inspect.py

from github import Github
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("GITHUB_TOKEN")
g = Github(token)

def list_branches(repo_name):
    """Return a list of all branches in the given repository"""
    try:
        repo = g.get_repo(repo_name)
        branches = repo.get_branches()
        return [branch.name for branch in branches]
    except Exception as e:
        return f"[ERROR] Failed to fetch branches: {str(e)}"

def list_recent_commits(repo_name, count=5):
    """List the latest commits in the given repo"""
    try:
        repo = g.get_repo(repo_name)
        commits = repo.get_commits()
        result = []
        for commit in commits[:count]:
            sha = commit.sha[:7]
            msg = commit.commit.message.split("\n")[0]
            author = commit.commit.author.name
            date = commit.commit.author.date.strftime('%Y-%m-%d %H:%M')
            result.append(f"{sha} | {author} | {date} | {msg}")
        return result
    except Exception as e:
        return f"[ERROR] Failed to fetch commits: {str(e)}"


def get_commit_diff(repo_name, commit_sha):
    """Get file changes and stats for a specific commit"""
    try:
        repo = g.get_repo(repo_name)
        commit = repo.get_commit(sha=commit_sha)
        files = commit.files
        summary = {
            "message": commit.commit.message,
            "author": commit.commit.author.name,
            "email": commit.commit.author.email,
            "github_user": commit.author.login if commit.author else "N/A",
            "github_url": commit.author.html_url if commit.author else "N/A",
            "date": commit.commit.author.date.strftime('%Y-%m-%d %H:%M'),
            "stats": {
                        "additions": commit.stats.additions,
                        "deletions": commit.stats.deletions,
                        "total": commit.stats.total
                    },
            "files_changed": []
        }
        for f in files:
            summary["files_changed"].append({
                "filename": f.filename,
                "additions": f.additions,
                "deletions": f.deletions,
                "changes": f.changes
            })
        return summary
    except Exception as e:
        return f"[ERROR] Failed to get commit diff: {str(e)}"
