
# 🚀 GitHub MCP: Model Context Protocol Client Toolkit

Welcome to **GitHub-MCP**, a robust and intelligent Python-based command-line interface (CLI) tool that brings the power of GitHub and the **Model Context Protocol (MCP)** together. This project bridges developer productivity and AI-driven automation by enabling seamless exploration, interaction, and modification of GitHub repositories using MCP standards.

---

## 📌 Table of Contents
- [🔍 Project Overview](#-project-overview)
- [⚙️ Features](#️-features)
- [🛠️ Technologies Used](#️-technologies-used)
- [🧠 How It Works](#-how-it-works)
- [📦 Installation](#-installation)
- [🚀 Usage](#-usage)
- [📚 References](#-references)
- [🙌 Acknowledgements](#-acknowledgements)

---

## 🔍 Project Overview

**GitHub-MCP** is a CLI-based project designed to **fetch, analyze, and manage GitHub repositories using AI-native protocols**. It is built with a vision of integrating [Model Configuration Protocol (MCP)](https://modelcontextprotocol.io) into daily GitHub workflows, enabling smart IDE-like AI capabilities directly through the terminal.

> From listing repositories to analyzing commits, managing pull requests, issues, branches, file trees, and file contents — this tool is your personal GitHub assistant powered by AI context.

---

## ⚙️ Features

| Feature | Description |
|--------|-------------|
| 🔍 Repository Search | List and match GitHub repositories interactively |
| 📊 Repo Stats | View forks, stars, issues, and description |
| 🚀 Pull Requests | Create, merge, and comment on PRs |
| 🐛 Issues | List open/closed issues and comment |
| 🧾 Commits | View commit history, file diffs, author metadata |
| 🌿 Branches | List all branches in a repo |
| 🗂️ File Tree | Explore repository tree and file structures |
| 📄 File Viewer | View file contents across branches |
| 🔐 Authenticated Access | Uses Personal Access Token (PAT) for extended GitHub API quota |

---

## 🛠️ Technologies Used

- **Python 3.10+**
- `PyGithub` - GitHub API SDK for Python
- `Rich` - Pretty CLI outputs
- **Model Configuration Protocol** - For standardizing and enabling structured repo context exchange (future integration)
- GitHub REST APIs

---

## 🧠 How It Works

This CLI tool connects to GitHub using a user-provided **Personal Access Token (PAT)** and enables:

1. **Interactive Repo Discovery:** List all repos, select one using keyword or full name.
2. **Metadata Fetching:** Pull stats, commits, README content, and branch info.
3. **Pull Request Control:** Create, merge, and comment on PRs via API.
4. **Issue Manager:** View issues, post comments, review threads.
5. **Commit Intelligence:** Fetch diffs, show line changes, authorship, and time.
6. **MCP Mapping (Phase 6+):** Uses [MCP schema](https://modelcontextprotocol.io/examples) to convert repo content into AI-readable structured contexts.

---

## 📦 Installation

```bash
git clone https://github.com/dhyeyinf/Github-MCP.git
cd Github-MCP
pip install -r requirements.txt
```

> 🔑 Make sure to export your PAT (Personal Access Token) before running:
```bash
export GITHUB_TOKEN="your_pat_here"
```

---

## 🚀 Usage

```bash
python main.py
```

> You will be guided through a sequence of inputs to interact with your GitHub data.

---

## 📚 References

This project is heavily inspired and aligned with the official MCP ecosystem:

- 🌐 [Model Context Protocol - Official Site](https://modelcontextprotocol.io)
- 📘 [MCP Examples](https://modelcontextprotocol.io/examples)
- 🧠 [Building MCP with LLMs](https://modelcontextprotocol.io/tutorials/building-mcp-with-llms)
- 📦 [GitHub MCP Server (Reference)](https://github.com/github/github-mcp-server)
- 🔗 [ModelContextProtocol GitHub](https://github.com/modelcontextprotocol)

---

## 🙌 Acknowledgements

Built as part of an advanced developer tools showcase by **Dhyey Findoriya**, integrating modern open-source standards with future-facing AI protocols. Special thanks to:

- GitHub Developer Ecosystem Team
- ModelContextProtocol maintainers
- PyGithub & open-source contributors

---

> 🧠 If you're building LLM copilots or repo-aware agents, GitHub-MCP is your launchpad. Feel free to fork, extend, or contribute!
