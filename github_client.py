# github_client.py

import os
from github import Github
from dotenv import load_dotenv

load_dotenv()

# Load the token
token = os.getenv("GITHUB_TOKEN")
if not token:
    raise ValueError("GITHUB_TOKEN not found in .env")

# GitHub client
g = Github(token)

def list_user_repos():
    """List your GitHub repositories"""
    user = g.get_user()
    return [repo.full_name for repo in user.get_repos()]

def get_repo_stats(repo_name):
    """Get basic stats for a repo"""
    repo = g.get_repo(repo_name)
    return {
        "name": repo.full_name,
        "description": repo.description,
        "stars": repo.stargazers_count,
        "forks": repo.forks_count,
        "open_issues": repo.open_issues_count,
    }

def list_pull_requests(repo_name):
    """List open pull requests in a repo"""
    repo = g.get_repo(repo_name)
    return [(pr.number, pr.title) for pr in repo.get_pulls(state='open')]

def get_file_content(repo_name, path):
    """Fetch a file from the repo"""
    repo = g.get_repo(repo_name)
    try:
        file_content = repo.get_contents(path)
        return file_content.decoded_content.decode()
    except Exception as e:
        return f"[ERROR] Could not fetch '{path}': {str(e)}"
