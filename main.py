# main.py
from review_pr import comment_on_pull_request
from github_client import list_user_repos, get_repo_stats, list_pull_requests, get_file_content
from pull_request_ops import create_pull_request
from merge_pr import merge_pull_request

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