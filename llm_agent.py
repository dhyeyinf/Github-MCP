# llm_agent.py
import requests
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "openrouter/cypher-alpha:free"

def load_context(path="mcp.json"):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e)}

def ask_llm(prompt, repo_name):
    """
    Query OpenRouter LLM to parse natural language commands and map to GitHub actions.
    Returns a JSON string with intent and parameters.
    """
    if not OPENROUTER_API_KEY:
        raise Exception("OPENROUTER_API_KEY not set in environment variables")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your-app-url.com",  # Replace with your app URL
        "X-Title": "GitHub MCP"
    }

    system_prompt = f"""
You are an AI assistant for a GitHub repository management tool. Your task is to parse natural language commands related to GitHub operations for the repository '{repo_name}' and return a JSON object with an 'intent' and 'params' for execution. Supported intents include:
- create_pr: Create a pull request (params: head, base, title, body)
- merge_pr: Merge a pull request (params: pr_number, message)
- comment_pr: Comment on a pull request (params: pr_number, comment)
- create_issue: Create an issue (params: title, body)
- comment_issue: Comment on an issue (params: issue_number, comment)
- list_items: List issues, pull requests, branches, or commits (params: state, item_type)
- view_file: View file content (params: file_path, branch)
- view_commit: View commit details (params: commit_sha)
- list_issue_comments: List comments on an issue (params: issue_number)
- repo_summary: Summarize the repository (no params)

For ambiguous commands (e.g., 'create a new pull request in this repo'), assume reasonable defaults (head='feature', base='main', title='PR for {repo_name}', body=''). Return JSON like:
```json
{"intent": "create_pr", "params": {"head": "feature", "base": "main", "title": "PR for repo", "body": ""}}
```
or
```json
{"error": "Could not understand command"}
```
Command: {prompt}
"""
    
    data = {
        "model": "meta-ai/llama-3.1-8b-instruct:free",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        raise Exception(f"OpenRouter API failed: {str(e)}")