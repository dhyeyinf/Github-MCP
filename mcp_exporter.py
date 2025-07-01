# mcp_exporter.py

from github import Github
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
g = Github(os.getenv("GITHUB_TOKEN"))

def generate_mcp_context(repo_name: str) -> dict:
    try:
        repo = g.get_repo(repo_name)

        # Safely fetch contributors
        try:
            contributors = repo.get_contributors()[:5]
            contributors_list = [
                {
                    "login": c.login,
                    "html_url": c.html_url,
                    "contributions": c.contributions
                } for c in contributors
            ]
        except Exception:
            contributors_list = []

        # Safely fetch commits
        try:
            commits = repo.get_commits()[:5]
            commits_list = [
                {
                    "sha": c.sha,
                    "author": c.commit.author.name if c.commit.author else "Unknown",
                    "message": c.commit.message.split('\n')[0],
                    "date": c.commit.author.date.strftime("%Y-%m-%d")
                } for c in commits
            ]
        except Exception:
            commits_list = []

        # Safely fetch issues
        try:
            issues = repo.get_issues(state="open")[:5]
            issues_list = [
                {
                    "number": i.number,
                    "title": i.title,
                    "created_at": i.created_at.strftime("%Y-%m-%d"),
                    "user": i.user.login if i.user else "Unknown"
                } for i in issues
            ]
        except Exception:
            issues_list = []

        # Safely fetch pull requests
        try:
            pull_requests = repo.get_pulls(state="open")[:5]
            prs_list = [
                {
                    "number": pr.number,
                    "title": pr.title,
                    "created_at": pr.created_at.strftime("%Y-%m-%d"),
                    "user": pr.user.login if pr.user else "Unknown"
                } for pr in pull_requests
            ]
        except Exception:
            prs_list = []

        # Final MCP object
        mcp = {
            "@context": "https://modelcontextprotocol.io/context/v1",
            "modelcontext": {
                "repository": {
                    "name": repo.full_name,
                    "description": repo.description,
                    "url": repo.html_url,
                    "stars": repo.stargazers_count,
                    "forks": repo.forks_count,
                    "topics": repo.get_topics(),
                    "created_at": repo.created_at.strftime("%Y-%m-%d"),
                    "updated_at": repo.updated_at.strftime("%Y-%m-%d"),
                },
                "contributors": contributors_list,
                "recent_commits": commits_list,
                "open_issues": issues_list,
                "open_pull_requests": prs_list
            }
        }

        return mcp

    except Exception as e:
        return {"error": str(e)}
