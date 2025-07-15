from github_client import list_user_repos, get_repo_stats, list_pull_requests, get_file_content
from pull_request_ops import create_pull_request
from merge_pr import merge_pull_request
from review_pr import comment_on_pull_request
from issues_client import create_issue, add_issue_comment, list_issues, list_issue_comments
from repo_inspect import list_branches, list_recent_commits, get_file_tree, get_commit_diff
import re
from datetime import datetime

def mock_llm(prompt, repo_name):
    """
    Mock LLM to parse natural language commands and map to GitHub actions.
    Returns a structured JSON with intent and parameters.
    """
    prompt = prompt.lower().strip()
    
    # Patterns for common commands
    patterns = [
        {
            "pattern": r"create (?:a )?(?:new )?pull request from (\w+) to (\w+)(?: with title ['\"](.+)['\"])?(?: and description ['\"](.+)['\"])?",
            "intent": "create_pr",
            "params": ["head", "base", "title", "body"]
        },
        {
            "pattern": r"merge pull request #?(\d+)(?: with message ['\"](.+)['\"])?",
            "intent": "merge_pr",
            "params": ["pr_number", "message"]
        },
        {
            "pattern": r"comment on pull request #?(\d+) with ['\"](.+)['\"]",
            "intent": "comment_pr",
            "params": ["pr_number", "comment"]
        },
        {
            "pattern": r"create (?:a )?(?:new )?issue(?: with title ['\"](.+)['\"])?(?: and body ['\"](.+)['\"])?",
            "intent": "create_issue",
            "params": ["title", "body"]
        },
        {
            "pattern": r"comment on issue #?(\d+) with ['\"](.+)['\"]",
            "intent": "comment_issue",
            "params": ["issue_number", "comment"]
        },
        {
            "pattern": r"list (open|closed)? ?(issues|pull requests|branches|commits)(?: of this repositor(?:y|ies))?",
            "intent": "list_items",
            "params": ["state", "item_type"]
        },
        {
            "pattern": r"view file ['\"](.+)['\"](?: on branch (\w+))?",
            "intent": "view_file",
            "params": ["file_path", "branch"]
        },
        {
            "pattern": r"view commit #?(\w+)",
            "intent": "view_commit",
            "params": ["commit_sha"]
        },
        {
            "pattern": r"list comments on issue #?(\d+)",
            "intent": "list_issue_comments",
            "params": ["issue_number"]
        },
    ]
    
    for p in patterns:
        match = re.match(p["pattern"], prompt)
        if match:
            result = {"intent": p["intent"], "params": {}}
            for param, value in zip(p["params"], match.groups()):
                if value:
                    result["params"][param] = value
            # Set defaults for optional params
            if p["intent"] == "create_pr" and "title" not in result["params"]:
                result["params"]["title"] = f"PR from {result['params']['head']} to {result['params']['base']}"
                result["params"]["body"] = result["params"].get("body", "")
            if p["intent"] == "merge_pr" and "message" not in result["params"]:
                result["params"]["message"] = "Merged via MCP"
            if p["intent"] == "create_issue" and "title" not in result["params"]:
                result["params"]["title"] = f"Issue created on {datetime.now().strftime('%Y-%m-%d')}"
                result["params"]["body"] = result["params"].get("body", "")
            if p["intent"] == "view_file" and "branch" not in result["params"]:
                result["params"]["branch"] = "main"
            if p["intent"] == "list_items" and "state" not in result["params"]:
                result["params"]["state"] = "open"
            return result
    
    return {"error": f"Could not understand command: {prompt}"}

def interpret_command(command, repo_name):
    """
    Parse natural language command using the mock LLM.
    Returns structured JSON with intent and parameters.
    """
    return mock_llm(command, repo_name)

def execute_actions(structured, repo_name):
    """
    Execute GitHub actions based on parsed intent and parameters.
    Returns a dictionary with 'message' and optional 'data' or 'error'.
    """
    intent = structured.get("intent")
    params = structured.get("params", {})
    
    try:
        if intent == "create_pr":
            result = create_pull_request(
                repo_name,
                params["base"],
                params["head"],
                params["title"],
                params.get("body", "")
            )
            return {"message": result.get("message", "Pull request created"), "data": result}
        
        elif intent == "merge_pr":
            result = merge_pull_request(
                repo_name,
                int(params["pr_number"]),
                params["message"]
            )
            return {"message": result.get("message", "Pull request merged"), "data": result}
        
        elif intent == "comment_pr":
            result = comment_on_pull_request(
                repo_name,
                int(params["pr_number"]),
                params["comment"]
            )
            return {"message": result.get("message", "Comment added to PR"), "data": result}
        
        elif intent == "create_issue":
            result = create_issue(
                repo_name,
                params["title"],
                params.get("body", "")
            )
            return {"message": result.get("message", "Issue created"), "data": result}
        
        elif intent == "comment_issue":
            result = add_issue_comment(
                repo_name,
                int(params["issue_number"]),
                params["comment"]
            )
            return {"message": result.get("message", "Comment added to issue"), "data": result}
        
        elif intent == "list_items":
            item_type = params["item_type"]
            state = params.get("state", "open")
            
            if item_type == "issues":
                data = list_issues(repo_name, state=state)
                return {"message": f"Listed {state} issues", "data": data}
            elif item_type == "pull requests":
                data = list_pull_requests(repo_name)
                return {"message": "Listed pull requests", "data": data}
            elif item_type == "branches":
                data = list_branches(repo_name)
                return {"message": "Listed branches", "data": data}
            elif item_type == "commits":
                data = list_recent_commits(repo_name)
                return {"message": "Listed recent commits", "data": data}
        
        elif intent == "view_file":
            content = get_file_content(
                repo_name,
                params["file_path"],
                branch=params["branch"]
            )
            if isinstance(content, str):
                return {"message": "File content retrieved", "data": {"content": content[:1000]}}
            else:
                return {"error": "Could not retrieve file content"}
        
        elif intent == "view_commit":
            summary = get_commit_diff(repo_name, params["commit_sha"])
            if isinstance(summary, str):
                return {"error": summary}
            else:
                return {"message": "Commit details retrieved", "data": summary}
        
        elif intent == "list_issue_comments":
            comments = list_issue_comments(repo_name, int(params["issue_number"]))
            if isinstance(comments, str):
                return {"error": comments}
            else:
                return {"message": f"Comments for issue #{params['issue_number']}", "data": comments}
        
        else:
            return {"error": f"Unknown intent: {intent}"}
    
    except Exception as e:
        return {"error": f"Action failed: {str(e)}"}