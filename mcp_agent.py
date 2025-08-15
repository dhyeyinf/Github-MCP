# mcp_agent.py

import json

def load_mcp_context(path="mcp.json"):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e)}

def run_agent_query(question: str):
    context = load_mcp_context()
    if "error" in context:
        return f"[ERROR] Could not load MCP context: {context['error']}"

    mc = context.get("modelcontext", {})
    repo = mc.get("repository", {})
    contributors = mc.get("contributors", [])
    commits = mc.get("recent_commits", [])
    issues = mc.get("open_issues", [])
    prs = mc.get("open_pull_requests", [])

    q = question.lower()

    if "top contributor" in q or "contributors" in q:
        return "\n".join([f"- {c['login']} ({c['contributions']} contributions)" for c in contributors]) or "No contributors found."

    elif "open issue" in q:
        return "\n".join([f"- #{i['number']}: {i['title']}" for i in issues]) or "No open issues."

    elif "pull request" in q or "open pr" in q:
        return "\n".join([f"- #{p['number']}: {p['title']}" for p in prs]) or "No open pull requests."

    elif "recent commit" in q or "commits" in q:
        return "\n".join([f"- {c['sha']} | {c['author']} | {c['date']} | {c['message']}" for c in commits]) or "No recent commits."
    elif "describe" in q or "summary" in q or "what is this repo" in q:
        return f"{repo.get('name')} — {repo.get('description') or 'No description provided.'}"

    else:
        return "❌ Sorry, I couldn't understand the question. Try asking about contributors, issues, PRs, commits, or repo info."
