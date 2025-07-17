import streamlit as st
from github_client import (
    list_user_repos, get_repo_stats, list_pull_requests, get_file_content,
    get_repo_topics, add_repo_topics, get_repo_license, update_repo_description, get_repo_summary
)
from pull_request_ops import create_pull_request
from merge_pr import merge_pull_request
from review_pr import comment_on_pull_request
from repo_inspect import list_branches, list_recent_commits, get_commit_diff, get_file_tree
from issues_client import list_issues, list_issue_comments, add_issue_comment, create_issue
from mcp_exporter import generate_mcp_context
from nlp_executor import interpret_command, execute_actions
import json
from datetime import datetime

# Streamlit App
st.set_page_config(page_title="GitHub MCP", layout="wide")

# Initialize session state
if "repo" not in st.session_state:
    st.session_state.repo = None
if "repos" not in st.session_state:
    st.session_state.repos = list_user_repos()

# Sidebar: Repository Selection
st.sidebar.header("Select Repository")
repo_names = [repo for repo in st.session_state.repos]
selected_repo = st.sidebar.selectbox("Choose a repository", repo_names, index=0)
if selected_repo:
    st.session_state.repo = selected_repo

# Main Content
st.title("GitHub MCP: AI-Powered Repository Management")
st.markdown("Interact with your GitHub repositories using natural language commands powered by an LLM.")

if st.session_state.repo:
    repo = st.session_state.repo
    st.header(f"Repository: {repo}")
    
    # Display Repo Stats
    with st.expander("Repository Stats", expanded=True):
        stats = get_repo_stats(repo)
        cols = st.columns(4)
        cols[0].metric("Stars", stats.get("stars", 0))
        cols[1].metric("Forks", stats.get("forks", 0))
        cols[2].metric("Open Issues", stats.get("open_issues", 0))
        cols[3].metric("Watchers", stats.get("watchers", 0))
    
    # Tabs for different views
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Natural Language Interface", "Pull Requests", "Issues", "Commits", "Files & Branches"])
    
    with tab1:
        st.subheader("Natural Language Commands")
        st.markdown("Enter commands like: 'Create a pull request from dev to main with title \"New Feature\"', 'List open issues', 'Comment on issue #5 with \"Looks good\"', 'View commit abc123', or 'Give me a summary of the repo'.")
        command = st.text_input("Enter your command:")
        if st.button("Execute Command"):
            if command:
                with st.spinner("Processing command..."):
                    structured = interpret_command(command, repo)
                    if "error" in structured:
                        st.error(structured["error"])
                    else:
                        result = execute_actions(structured, repo)
                        if "error" in result:
                            st.error(result["error"])
                        else:
                            st.success(result["message"])
                            if "data" in result:
                                if structured.get("intent") == "list_items" and structured.get("params", {}).get("item_type") == "issues":
                                    for issue in result["data"]:
                                        st.write(f"#{issue['number']}: {issue['title']} by {issue['creator']} at {issue['created_at']}")
                                elif structured.get("intent") == "repo_summary":
                                    summary = result["data"]
                                    st.markdown(f"""
**Repository Summary for {summary['name']}**
- **Description**: {summary['description']}
- **Stars**: {summary['stars']}
- **Forks**: {summary['forks']}
- **Open Issues**: {summary['open_issues']}
- **Open PRs**: {summary['open_prs']}
- **Recent Commits (last 5)**: {summary['recent_commits']}
- **Topics**: {', '.join(summary['topics'])}
- **Created**: {summary['created_at']}
- **Last Updated**: {summary['last_updated']}
""")
                                else:
                                    st.json(result["data"])
    
    with tab2:
        st.subheader("Pull Requests")
        prs = list_pull_requests(repo)
        if not prs:
            st.write("No open pull requests.")
        else:
            for number, title in prs:
                st.write(f"PR #{number}: {title}")
        
        with st.form("create_pr_form"):
            st.markdown("### Create Pull Request")
            base = st.text_input("Base branch", "main")
            head = st.text_input("Head branch", "feature")
            title = st.text_input("PR Title")
            body = st.text_area("PR Description (optional)")
            if st.form_submit_button("Create PR"):
                result = create_pull_request(repo, base, head, title, body)
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success(result["message"])
        
        if prs:
            with st.form("merge_pr_form"):
                st.markdown("### Merge Pull Request")
                pr_num = st.selectbox("Select PR to merge", [num for num, _ in prs])
                merge_message = st.text_input("Merge commit message", "Merged via MCP")
                if st.form_submit_button("Merge PR"):
                    result = merge_pull_request(repo, pr_num, merge_message)
                    if "error" in result:
                        st.error(result["error"])
                    else:
                        st.success(result["message"])
            
            with st.form("comment_pr_form"):
                st.markdown("### Comment on Pull Request")
                pr_num = st.selectbox("Select PR to comment", [num for num, _ in prs], key="comment_pr_select")
                comment = st.text_area("Comment")
                if st.form_submit_button("Add Comment"):
                    result = comment_on_pull_request(repo, pr_num, comment)
                    if "error" in result:
                        st.error(result["error"])
                    else:
                        st.success(result["message"])
    
    with tab3:
        st.subheader("Issues")
        open_issues = list_issues(repo, state="open")
        closed_issues = list_issues(repo, state="closed")
        
        st.markdown("### Open Issues")
        if not open_issues:
            st.write("No open issues.")
        else:
            for issue in open_issues:
                with st.expander(f"#{issue['number']}: {issue['title']} by {issue['creator']} at {issue['created_at']}"):
                    comments = list_issue_comments(repo, issue['number'])
                    if isinstance(comments, str):
                        st.error(comments)
                    elif not comments:
                        st.write("No comments yet.")
                    else:
                        st.markdown("#### Comments")
                        for c in comments:
                            st.write(f"- {c['user']} at {c['created_at']}: {c['body']}")
        
        st.markdown("### Closed Issues")
        if not closed_issues:
            st.write("No closed issues.")
        else:
            for issue in closed_issues:
                with st.expander(f"#{issue['number']}: {issue['title']} by {issue['creator']} at {issue['created_at']}"):
                    comments = list_issue_comments(repo, issue['number'])
                    if isinstance(comments, str):
                        st.error(comments)
                    elif not comments:
                        st.write("No comments yet.")
                    else:
                        st.markdown("#### Comments")
                        for c in comments:
                            st.write(f"- {c['user']} at {c['created_at']}: {c['body']}")
        
        with st.form("create_issue_form"):
            st.markdown("### Create Issue")
            issue_title = st.text_input("Issue Title")
            issue_body = st.text_area("Issue Description")
            if st.form_submit_button("Create Issue"):
                result = create_issue(repo, issue_title, issue_body)
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success(result["message"])
        
        with st.form("comment_issue_form"):
            st.markdown("### Comment on Issue")
            issue_numbers = [issue['number'] for issue in open_issues + closed_issues]
            if not issue_numbers:
                st.write("No issues available to comment on.")
            else:
                issue_num = st.selectbox("Select Issue", issue_numbers)
                comment = st.text_area("Issue Comment")
                if st.form_submit_button("Add Comment"):
                    result = add_issue_comment(repo, issue_num, comment)
                    if "error" in result:
                        st.error(result["error"])
                    else:
                        st.success(result["message"])
    
    with tab4:
        st.subheader("Commits")
        commits = list_recent_commits(repo)
        if isinstance(commits, str):
            st.error(commits)
        else:
            for c in commits:
                with st.expander(f"{c['sha'][:7]} | {c['author']} | {c['date']} | {c['message']}"):
                    if st.button("View Details", key=f"commit_{c['sha']}"):
                        summary = get_commit_diff(repo, c['sha'])
                        if isinstance(summary, str):
                            st.error(summary)
                        else:
                            st.markdown(f"**Commit Message**: {summary['message']}")
                            st.markdown(f"**Author**: {summary['author']} on {summary['date']}")
                            st.markdown(f"**Email**: {summary['email']}")
                            st.markdown(f"**GitHub**: [{summary['github_user']}]({summary['github_url']})")
                            st.markdown(f"**Stats**: Additions: {summary['stats']['additions']}, Deletions: {summary['stats']['deletions']}, Total: {summary['stats']['total']}")
                            st.markdown("**Files Changed**:")
                            for f in summary["files_changed"]:
                                st.write(f"- {f['filename']} (+{f['additions']}/-{f['deletions']})")
    
    with tab5:
        st.subheader("Files & Branches")
        branches = list_branches(repo)
        if isinstance(branches, str):
            st.error(branches)
        else:
            selected_branch = st.selectbox("Select Branch", branches, key="file_branch")
            tree = get_file_tree(repo, branch=selected_branch)
            if isinstance(tree, str):
                st.error(tree)
            elif not tree:
                st.write("No files found.")
            else:
                st.markdown("### File Tree")
                for item in tree:
                    emoji = "📄" if item["type"] == "file" else "📁"
                    st.write(f"{emoji} {item['path']}")
                
                file_path = st.text_input("Enter file path to view content")
                if st.button("View File Content"):
                    content = get_file_content(repo, file_path, branch=selected_branch)
                    if isinstance(content, str):
                        st.code(content[:1000], language="text")
                    else:
                        st.error("Could not retrieve file content.")
    
    # Topics and License
    with st.expander("Repository Metadata"):
        st.markdown("### Topics")
        topics = get_repo_topics(repo)
        if isinstance(topics, str):
            st.error(topics)
        else:
            st.write(", ".join(topics) if topics else "No topics found.")
        
        new_topics = st.text_input("Add new topics (comma-separated)")
        if st.button("Update Topics"):
            if new_topics:
                new_topics_list = [t.strip() for t in new_topics.split(",") if t.strip()]
                result = add_repo_topics(repo, new_topics_list)
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success(result["message"])
        
        st.markdown("### License")
        license_info = get_repo_license(repo)
        st.write(license_info)
        
        st.markdown("### Description")
        new_desc = st.text_area("Update repository description", stats.get("description", ""))
        if st.button("Update Description"):
            result = update_repo_description(repo, new_desc)
            if "error" in result:
                st.error(result["error"])
            else:
                st.success(result["message"])
    
    # MCP Context File
    if st.button("Generate MCP Context File (mcp.json)"):
        mcp = generate_mcp_context(repo)
        if "error" in mcp:
            st.error(f"Failed to generate MCP context: {mcp['error']}")
        else:
            with open("mcp.json", "w") as f:
                json.dump(mcp, f, indent=4)
            st.success("MCP context file saved as mcp.json")
            st.download_button(
                label="Download mcp.json",
                data=json.dumps(mcp, indent=4),
                file_name="mcp.json",
                mime="application/json"
            )

else:
    st.warning("Please select a repository from the sidebar.")