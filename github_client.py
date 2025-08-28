# github_client.py
import os
import base64
import requests
from github import Github, GithubException
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.github.com"
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

# print("GitHub client initialized.")
def list_pull_requests(repo_name):
    """List open pull requests in a repo"""
    repo = g.get_repo(repo_name)
    return [(pr.number, pr.title) for pr in repo.get_pulls(state='open')]

def get_file_content(repo_full_name, path, branch=None):
    try:
        repo = g.get_repo(repo_full_name)
        if branch:
            file_content = repo.get_contents(path, ref=branch)
        else:
            file_content = repo.get_contents(path)
        return base64.b64decode(file_content.content).decode()
    except Exception as e:
        return f"❌ Error fetching file content: {e}"

def get_repo_topics(repo_full_name):
    try:
        repo = g.get_repo(repo_full_name)
        return repo.get_topics()
    except GithubException as e:
        return f"❌ Error fetching topics: {e.data.get('message', str(e))}"

def add_repo_topics(repo_full_name, new_topics):
    try:
        repo = g.get_repo(repo_full_name)
        existing_topics = repo.get_topics()
        all_topics = list(set(existing_topics + new_topics))
        repo.replace_topics(all_topics)
        return f"✅ Topics updated: {', '.join(all_topics)}"
    except GithubException as e:
        return f"❌ Error adding topics: {e.data.get('message', str(e))}"

def get_repo_license(repo_full_name):
    try:
        repo = g.get_repo(repo_full_name)
        return repo.get_license().license.name
    except GithubException as e:
        return f"❌ Error fetching license: {e.data.get('message', str(e))}"

def update_repo_description(repo_full_name, new_description):
    url = f"{BASE_URL}/repos/{repo_full_name}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }
    response = requests.patch(
        url,
        headers=headers,
        json={"description": new_description}
    )

    if response.status_code == 200:
        return f"✅ Description updated to: {new_description}"
    else:
        return f"❌ Failed to update description: {response.json().get('message', 'Unknown error')}"

def get_repo_summary(repo_name):
    """
    Generate a summary of the repository including stats, topics, and recent activity.
    """
    try:
        repo = g.get_repo(repo_name)
        stats = get_repo_stats(repo_name)
        topics = repo.get_topics()
        open_issues = len([i for i in repo.get_issues(state="open") if i.pull_request is None])
        open_prs = len(list(repo.get_pulls(state="open")))
        recent_commits = len(list(repo.get_commits()[:5]))
        
        summary = {
            "name": stats.get("name", repo_name),
            "description": stats.get("description", "No description available"),
            "stars": stats.get("stars", 0),
            "forks": stats.get("forks", 0),
            "open_issues": open_issues,
            "open_prs": open_prs,
            "recent_commits": recent_commits,
            "topics": topics if topics else ["None"],
            "created_at": repo.created_at.strftime('%Y-%m-%d'),
            "last_updated": repo.updated_at.strftime('%Y-%m-%d')
        }
        return summary
    except Exception as e:
        return f"[ERROR] Failed to generate repo summary: {str(e)}"
