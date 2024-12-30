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

### Install Dependencies:
You can install the required dependencies using the following command:

```bash
pip install -r requirements.txt

# GitHub Token Setup

To interact with the GitHub API, you will need a GitHub personal access token.

1. Go to GitHub: [GitHub Personal Access Tokens](https://github.com/settings/tokens)
2. Create a new token with the required permissions (repo, user, etc.).
3. Set the token as an environment variable in your terminal:

   ```bash
   export GITHUB_TOKEN="your_personal_access_token"

This token will allow the project to authenticate with GitHub and fetch pull requests.

## How to Use

1. **Set up the environment:**
   - Clone the repository and set up a Python virtual environment:

     ```bash
     git clone https://github.com/yourusername/AI_Code_Review.git
     cd AI_Code_Review
     python -m venv .venv
     source .venv/bin/activate
     ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt

## 3. Run the script

You can run the analysis by executing the `fetch_pull_requests.py` script:

```bash
python fetch_pull_requests.py

## 4. Web Interface

You can view the results in the web interface by running the Flask application:

```bash
python app.py

Visit [http://localhost:5000](http://localhost:5000) to see the historical analysis results.

## Explanation of Key Terms

- **Pylint:** Pylint is a static code analysis tool for Python that looks for programming errors, helps enforce coding standards, and checks code quality.
- **PyGithub:** PyGithub is a Python library that allows you to interact with the GitHub API, enabling access to repositories, issues, pull requests, and much more.
- **Flask:** Flask is a micro web framework written in Python. It is used to build the web interface that displays analysis results.
- **CodeBERT:** CodeBERT is a pre-trained model by Microsoft, fine-tuned to perform code analysis tasks. It is based on the BERT architecture, specialized for code.
- **SQLite:** SQLite is a C-language library that implements a small, fast, self-contained, high-reliability, full-featured SQL database engine.
- **GitHub Actions:** GitHub Actions is a CI/CD tool that automates the process of running tests, deployments, and other workflows directly in GitHub.
- **SendGrid:** SendGrid is a cloud-based service used for sending email notifications. The project uses SendGrid to notify users about pull request analysis results.

## Email Notifications

Once the analysis is completed, the contributors will be notified via email about the analysis results, including:
- **Pylint Score:** Overall Pylint score (ranging from 0 to 10).
- **AI Feedback:** AI analysis feedback generated by the CodeBERT model.
- **Status:** Whether the pull request passed or failed based on the Pylint score.

The email will contain the following information:
- Status of the pull request analysis: Passed or Failed.
- Pylint score (overall rating).
- AI analysis results for each file in the pull request.

## Future Improvements

- **Model Fine-tuning:** Future versions of the project will include a more fine-tuned version of CodeBERT for more accurate analysis.
- **Dataset Augmentation:** We plan to expand and augment the dataset used for fine-tuning to improve the model’s performance.
- **Additional Integrations:** Further integrations with other code quality tools and services are planned to enhance the project’s functionality.
