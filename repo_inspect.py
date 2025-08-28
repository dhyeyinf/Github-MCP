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

def list_recent_commits(repo_name):
    """List recent commits in a repository"""
    try:
        repo = g.get_repo(repo_name)
        commits = repo.get_commits()[:7]  # Limit to 7 recent commits
        commit_list = []
        for commit in commits:
            commit_list.append({
                "sha": commit.sha,
                "author": commit.commit.author.name,
                "date": commit.commit.author.date.strftime('%Y-%m-%d %H:%M'),
                "message": commit.commit.message
            })
        return commit_list
    except Exception as e:
        return f"[ERROR] Failed to list commits: {str(e)}"


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
def get_file_tree(repo_name, branch="main", path=""):
    """Return the file/folder tree of a repo at a given branch and path"""
    try:
        repo = g.get_repo(repo_name)
        contents = repo.get_contents(path, ref=branch)
        file_list = []
        for content in contents:
            file_list.append({
                "name": content.name,
                "path": content.path,
                "type": content.type  # 'file' or 'dir'
            })
        return file_list
    except Exception as e:
        return f"[ERROR] Could not fetch file tree: {str(e)}"
