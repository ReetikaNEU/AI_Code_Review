import os
from github import Github

# Fetch the GitHub token from environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Check if the token is set
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN environment variable is not set! Please set it in your shell configuration.")

# Authenticate using the GitHub token
g = Github(GITHUB_TOKEN)

# Get repository details
REPO_NAME = "ReetikaNEU/AI_Code_Review"
repo = g.get_repo(REPO_NAME)

# Print repository full name
print(repo.full_name)