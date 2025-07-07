# nlp_executor.py

import os
import json
import requests
from repo_inspect import list_recent_commits
from pull_request_ops import create_pull_request

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = "deepseek/deepseek-chat-v3-0324:free"


def interpret_command(prompt: str, repo_name: str) -> dict:
    """
    Sends the natural language prompt to OpenRouter and receives structured actions.
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    f"You are a GitHub assistant for the repository '{repo_name}'. "
                    "Interpret the user's natural language request and return a valid JSON list of actions "
                    "you want to perform. Only respond in JSON. Each action can be:\n"
                    "- {\"action\": \"create_pr\", \"base\": \"main\", \"head\": \"dev\", \"title\": \"My PR Title\", \"body\": \"Optional body\"}\n"
                    "- {\"action\": \"list_commits\", \"count\": 3}\n"
                    "You must only respond with the JSON array of actions. Do not add explanations."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        try:
            raw = response.json()["choices"][0]["message"]["content"]
            return json.loads(raw)
        except Exception as e:
            return {"error": f"Failed to parse LLM response: {str(e)}"}
    else:
        return {"error": f"LLM failed: {response.text}"}


def execute_actions(actions: list, repo_name: str) -> str:
    """
    Executes the interpreted list of actions on the GitHub repo.
    """
    output = []
    for action in actions:
        try:
            if action["action"] == "create_pr":
                base = action["base"]
                head = action["head"]
                title = action["title"]
                body = action.get("body", "")
                result = create_pull_request(repo_name, base, head, title, body)
                output.append(f"🔀 Pull Request: {result}")

            elif action["action"] == "list_commits":
                count = action.get("count", 5)
                commits = list_recent_commits(repo_name, count)
                output.append("📜 Recent Commits:\n" + "\n".join(commits))

            else:
                output.append(f"⚠️ Unknown action: {action['action']}")
        except Exception as e:
            output.append(f"❌ Error executing action: {str(e)}")

    return "\n".join(output)
