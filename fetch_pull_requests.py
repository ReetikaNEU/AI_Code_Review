import os
from github import Github

# Fetch the GitHub token from environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Check if the token is set
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN environment variable is not set! Please set it in your shell configuration.")

# Authenticate with GitHub
g = Github(GITHUB_TOKEN)

# Specify the repository (e.g., "username/repository_name")
REPO_NAME = "ReetikaNEU/AI_Code_Review"

# Fetch the repository
repo = g.get_repo(REPO_NAME)

# Fetch open pull requests
pulls = repo.get_pulls(state='open', sort='created', base='main')

print(f"Open Pull Requests in {REPO_NAME}:")
for pr in pulls:
    print(f"- PR #{pr.number}: {pr.title} by {pr.user.login}")