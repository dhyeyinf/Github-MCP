# main.py

from github_client import list_user_repos, get_repo_stats, list_pull_requests, get_file_content

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
