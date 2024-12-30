# AI Code Review

## Overview
AI Code Review is an advanced static code analysis tool that integrates GitHub pull requests, Pylint, and AI-based analysis to review code changes in a repository. The tool uses the **Microsoft CodeBERT** model (and a fine-tuned version, to be integrated later) for code analysis and helps in evaluating code for quality, inefficiencies, and potential issues. This tool provides automated feedback on code quality, which helps developers ensure high-quality contributions.

## Problem Statement
As software development becomes more complex, reviewing code manually can be error-prone and time-consuming. This project addresses this by automating the code review process using AI and static analysis. The tool fetches pull requests from GitHub, analyzes the code using Pylint and AI models (like CodeBERT), and provides feedback on the quality of the code.

## Features

### 1. **GitHub Integration**
   - **Automatic Pull Request Fetching**: The project fetches open pull requests from a GitHub repository using the GitHub API.
   - **Pylint Integration**: It runs Pylint on changed files in the pull request and computes a Pylint score, helping developers identify potential issues in the code.

### 2. **AI-based Code Analysis**
   - **CodeBERT Integration**: The tool uses the Microsoft CodeBERT model (and a fine-tuned version, to be integrated later) to analyze code snippets for inefficiencies or potential issues.
   - **AI Scoring**: The AI model provides feedback based on the quality of the code, identifying potential inefficiencies.

### 3. **Database Integration**
   - **SQLite Database**: Historical analysis results are saved in an SQLite database for easy retrieval and display.
   - **Persistent Results**: The results of each pull request analysis are stored, including the Pylint score and AI-based analysis.

### 4. **Web Interface**
   - **User Interface**: The results of code analysis are displayed through a simple web interface built using **Flask**. Users can filter and sort the results based on different parameters like PR ID, author, or Pylint score.

### 5. **CI/CD Integration**
   - **GitHub Actions**: The project is integrated with GitHub Actions for Continuous Integration and Deployment (CI/CD). The GitHub Actions workflow automates the process of running the analysis script every time a new pull request is opened or updated.
   - **Automatic Status Updates**: The workflow automatically updates the status of the pull request on GitHub based on the results of the analysis.

### 6. **Email Notifications**
   - **Automated Email Alerts**: Contributors receive email notifications regarding the status of their pull request analysis. The email includes details about the overall Pylint score, AI analysis results, and whether the pull request passed or failed.

## Requirements

### Python Version:
- Python 3.11 (or any compatible version from 3.8 to 3.11)

### Dependencies:
The following Python libraries are required to run the project:

```txt
aiohappyeyeballs==2.4.4
aiohttp==3.11.11
aiosignal==1.3.2
astroid==3.3.8
attrs==24.3.0
blinker==1.9.0
certifi==2024.12.14
cffi==1.17.1
charset-normalizer==3.4.1
click==8.1.8
cryptography==44.0.0
Deprecated==1.2.15
dill==0.3.9
filelock==3.16.1
Flask==3.1.0
frozenlist==1.5.0
fsspec==2024.12.0
huggingface-hub==0.27.0
idna==3.10
isort==5.13.2
itsdangerous==2.2.0
Jinja2==3.1.5
MarkupSafe==3.0.2
mccabe==0.7.0
mpmath==1.3.0
multidict==6.1.0
networkx==3.4.2
numpy==1.23.5
packaging==24.2
platformdirs==4.3.6
propcache==0.2.1
pycparser==2.22
PyGithub==2.5.0
PyJWT==2.10.1
pylint==3.3.3
PyNaCl==1.5.0
python-http-client==3.3.7
PyYAML==6.0.2
regex==2024.11.6
requests==2.32.3
safetensors==0.4.5
sendgrid==6.11.0
starkbank-ecdsa==2.2.0
sympy==1.13.1
tabulate==0.9.0
tokenizers==0.21.0
tomlkit==0.13.2
torch==2.5.1
tqdm==4.67.1
transformers==4.47.1
typing_extensions==4.12.2
urllib3==2.3.0
Werkzeug==3.1.3
wrapt==1.17.0
yarl==1.18.3

You can install the required dependencies using the following command:

pip install -r requirements.txt

GitHub Token Setup

To interact with the GitHub API, you will need a GitHub personal access token.
	1.	Go to GitHub: GitHub Personal Access Tokens
	2.	Create a new token with the required permissions (repo, user, etc.).
	3.	Set the token as an environment variable:

export GITHUB_TOKEN="your_personal_access_token"



This token will allow the project to authenticate with GitHub and fetch pull requests.

How to Use

1. Set up the environment:
	•	Clone the repository and set up a Python virtual environment:

git clone https://github.com/yourusername/AI_Code_Review.git
cd AI_Code_Review
python -m venv .venv
source .venv/bin/activate

2. Install dependencies:

pip install -r requirements.txt

3. Run the script:

You can run the analysis by executing the fetch_pull_requests.py script:

python fetch_pull_requests.py

4. Web Interface:

You can view the results in the web interface by running the Flask application:

python app.py

Visit http://localhost:5000 to see the historical analysis results.

**Explanation of Key Terms**

Pylint - Pylint is a static code analysis tool for Python that looks for programming errors, helps enforce coding standards, and checks code quality.
PyGithub - PyGithub is a Python library that allows you to interact with the GitHub API, enabling access to repositories, issues, pull requests, and much more.
Flask - Flask is a micro web framework written in Python. It is used to build the web interface that displays analysis results.
CodeBERT - CodeBERT is a pre-trained deep learning model designed by Microsoft for code understanding and generation. It is based on the transformer architecture.
GitHub Actions - GitHub Actions is a CI/CD tool that automates workflows directly from GitHub repositories. It is used to run the analysis and other scripts automatically.
SQLite - SQLite is a C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine. It is used to store analysis results.
CI/CD - Continuous Integration and Continuous Deployment is a practice that involves automated code testing and deployment, ensuring code quality and fast delivery.

**User Notification**

After the code analysis is complete, users are notified via:
	1.	Email Notification: Contributors receive an email summarizing the pull request analysis results, including the Pylint score and AI analysis.
	2.	GitHub Status Update: A status check is added to the pull request to indicate whether the code quality passed or failed based on the analysis.
	3.	GitHub Issue Comment: A detailed comment is added to the pull request with the full analysis report, including Pylint and AI analysis, highlighting any issues.

**Future Improvements**
	•	Fine-tuning of CodeBERT: In the future, the model will be further fine-tuned for more accurate code analysis, especially for specific programming languages or use cases.
	•	Model Update: As the project evolves, a newer and more optimized version of CodeBERT will be integrated into the workflow to enhance the performance and accuracy of the analysis.

**Thank you for using AI Code Review!**
