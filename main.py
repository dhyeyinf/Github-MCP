# main.py
from review_pr import comment_on_pull_request
from github_client import list_user_repos, get_repo_stats, list_pull_requests, get_file_content
from pull_request_ops import create_pull_request
from merge_pr import merge_pull_request
from repo_inspect import list_branches
from repo_inspect import list_recent_commits
from repo_inspect import get_commit_diff
from issues_client import list_issues
from issues_client import list_issue_comments, add_issue_comment

# 🔁 Step 1: List all repos
repos = list_user_repos()
print("📦 Your Repositories:")
for idx, name in enumerate(repos, 1):
    print(f"{idx}. {name}")

# 🔍 Step 2: Ask user for input
user_prompt = input("\nEnter keyword or exact repo name to explore (e.g., 'ai', 'Brand-Monitoring'): ").lower()

# 🔎 Step 3: Try to match
matched_repo = None
for repo in repos:
    if user_prompt in repo.lower():
        matched_repo = repo
        break

print(f"\n🌿 Branches in {matched_repo}:")
branches = list_branches(matched_repo)
if isinstance(branches, list):
    for b in branches:
        print(f"  - {b}")
else:
    print(branches)  # show error message if any

print(f"\n📝 Latest Commits in {matched_repo}:")
commits = list_recent_commits(matched_repo)
if isinstance(commits, list):
    for c in commits:
        print(f"  - {c}")
else:
    print(commits)  # error message

# Ask if user wants commit details
view_diff = input("\nDo you want to view a commit's file changes? (yes/no): ").lower()
if view_diff == "yes":
    commit_sha = input("Enter the full or short SHA of the commit: ").strip()
    summary = get_commit_diff(matched_repo, commit_sha)
    
    if isinstance(summary, str):
        print(summary)  # error
    else:
        print(f"\n🔍 Commit Message: {summary['message']}")
        print(f"👤 Author: {summary['author']} on {summary['date']}")
        print(f"📧 Email: {summary['email']}")
        print(f"🔗 GitHub: {summary['github_user']} ({summary['github_url']})")
        print(f"📊 Stats — Additions: {summary['stats']['additions']}, Deletions: {summary['stats']['deletions']}, Total: {summary['stats']['total']}")
        print("📝 Files Changed:")
        for f in summary["files_changed"]:
            print(f"  - {f['filename']} (+{f['additions']}/-{f['deletions']})")

print(f"\n🐛 Open Issues in {matched_repo}:")
open_issues = list_issues(matched_repo, state="open")
if isinstance(open_issues, str):
    print(open_issues)
elif not open_issues:
    print("No open issues.")
else:
    for issue in open_issues:
        print(f"  - #{issue['number']}: {issue['title']} by {issue['creator']} at {issue['created_at']}")

print(f"\n📦 Closed Issues in {matched_repo}:")
closed_issues = list_issues(matched_repo, state="closed")
if isinstance(closed_issues, str):
    print(closed_issues)
elif not closed_issues:
    print("No closed issues.")
else:
    for issue in closed_issues:
        print(f"  - #{issue['number']}: {issue['title']} by {issue['creator']} at {issue['created_at']}")

# 🗣️ Ask user if they want to comment
add_comment = input("\nDo you want to view or comment on an issue? (yes/no): ").lower()
if add_comment == "yes":
    try:
        issue_number = int(input("Enter the issue number to work on: "))
        
        # Show existing comments
        comments = list_issue_comments(matched_repo, issue_number)
        if isinstance(comments, str):
            print(comments)
        elif not comments:
            print("No comments yet.")
        else:
            print("\n🧾 Comments:")
            for c in comments:
                print(f"  - {c['user']} at {c['created_at']}:\n    {c['body']}\n")

        # Ask if user wants to add one
        add_new = input("Do you want to add a new comment to this issue? (yes/no): ").lower()
        if add_new == "yes":
            comment_body = input("Enter your comment: ")
            result = add_issue_comment(matched_repo, issue_number, comment_body)
            print(result)

    except ValueError:
        print("❌ Please enter a valid numeric issue number.")


# ❌ No match
if not matched_repo:
    print("❌ No matching repository found.")
else:
    # ✅ Repo selected
    print(f"\n🧾 Repo Stats for {matched_repo}:")
    stats = get_repo_stats(matched_repo)
    for key, value in stats.items():
        print(f"{key}: {value}")

    print(f"\n🚀 Open Pull Requests for {matched_repo}:")
    prs = list_pull_requests(matched_repo)
    if not prs:
        print("No open PRs.")
    else:
        for number, title in prs:
            print(f"PR #{number}: {title}")

    print(f"\n📄 File Content (README.md from {matched_repo}):")
    content = get_file_content(matched_repo, "README.md")
    print(content[:500])  # Print first 500 chars

    # 📌 Phase 2.1: Create PR
    create_pr = input("\nDo you want to create a pull request for this repo? (yes/no): ").lower()
    if create_pr == "yes":
        base = input("Base branch (e.g., main): ")
        head = input("Head branch (feature branch): ")
        title = input("PR title: ")
        body = input("PR description (optional): ")
        result = create_pull_request(matched_repo, base, head, title, body)
        print(result)

        # 🔁 Refresh PR list after creation
        prs = list_pull_requests(matched_repo)

    # 📌 Phase 2.2: Merge PR
    if prs:  # Only allow merge if PRs exist
        merge_option = input("\nDo you want to merge a pull request? (yes/no): ").lower()
        if merge_option == "yes":
            print("Which PR do you want to merge?")
            for number, title in prs:
                print(f"  #{number}: {title}")
            
            try:
                pr_num = int(input("Enter the PR number exactly as shown above: "))
                valid_pr_numbers = [num for num, _ in prs]
                
                if pr_num not in valid_pr_numbers:
                    print("❌ Invalid PR number for this repo.")
                else:
                    message = input("Enter merge commit message (or leave blank): ") or "Merged via MCP script"
                    result = merge_pull_request(matched_repo, pr_num, message)
                    print(result)
            except ValueError:
                print("❌ Please enter a valid numeric PR number.")
    else:
        print("No open PRs to merge.")

    # Ask if user wants to comment on a PR
    if prs:  # Only show review option if PRs exist
        review_option = input("\nDo you want to add a comment to a pull request? (yes/no): ").lower()
        if review_option == "yes":
            print("Which PR do you want to comment on?")
            for number, title in prs:
                print(f"  #{number}: {title}")
            
            try:
                pr_num = int(input("Enter PR number: "))
                valid_pr_numbers = [num for num, _ in prs]
                
                if pr_num not in valid_pr_numbers:
                    print("❌ Invalid PR number.")
                else:
                    comment = input("Enter your comment: ")
                    result = comment_on_pull_request(matched_repo, pr_num, comment)
                    print(result)
            except ValueError:
                print("❌ Please enter a valid numeric PR number.")