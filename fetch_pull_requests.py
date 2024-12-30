import os
import sqlite3
from github import Github
import subprocess
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import re
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def load_model():
    """Load CodeBERT tokenizer and model."""
    tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
    model = AutoModelForSequenceClassification.from_pretrained("microsoft/codebert-base")
    return tokenizer, model


def analyze_code_with_ai(code_snippet, tokenizer, model):
    """Analyze code snippet for inefficiencies or issues using CodeBERT."""
    inputs = tokenizer(code_snippet, return_tensors="pt", max_length=512, truncation=True)
    outputs = model(**inputs)
    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    efficiency_score = predictions[0][0].item()  # Example: First class score
    issue_score = predictions[0][1].item()  # Example: Second class score

    # Interpret the results
    if efficiency_score > issue_score:
        return "Code seems efficient. No major issues detected."
    else:
        return "Code may have inefficiencies or potential issues to address."


def extract_pylint_score(output):
    """Extract the overall Pylint score from the output."""
    for line in output.splitlines():
        if "Your code has been rated at" in line:
            match = re.search(r"rated at ([0-9\.]+)/10", line)
            if match:
                try:
                    score = float(match.group(1))  # Extract and convert the score
                    return score
                except ValueError:
                    return None
    return None


def setup_database():
    """Set up SQLite database and table."""
    conn = sqlite3.connect("code_analysis.db")  # Connect to the database file
    cursor = conn.cursor()

    # Create the pull_request_analysis table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pull_request_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pull_request_id INTEGER,
            title TEXT,
            author TEXT,
            file_name TEXT,
            pylint_score REAL,
            ai_analysis TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_results_to_database(pr_id, title, author, file_name, pylint_score, ai_analysis):
    """Save analysis results to the SQLite database."""
    conn = sqlite3.connect("code_analysis.db")  # Connect to the database file
    cursor = conn.cursor()

    # Insert analysis results into the pull_request_analysis table
    cursor.execute("""
        INSERT INTO pull_request_analysis (
            pull_request_id, title, author, file_name, pylint_score, ai_analysis, timestamp
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (pr_id, title, author, file_name, pylint_score, ai_analysis, datetime.now().isoformat()))

    conn.commit()
    conn.close()


def create_status(repo, sha, state, description, context="Code Quality Check"):
    """Create a GitHub status check."""
    repo.get_commit(sha).create_status(
        state=state,  # "success" or "failure"
        description=description,
        context=context
    )


def send_email_notification(recipient_email, pr_id, status, overall_score):
    """Send email notification to the contributor."""
    sender_email = "your_email@example.com"  # Replace with your email
    sender_password = "your_password"  # Replace with your email password or app-specific password

    subject = f"PR #{pr_id}: Code Quality Check {'Passed' if status == 'success' else 'Failed'}"
    body = f"""
    Hello,

    Your Pull Request #{pr_id} has been analyzed.

    Status: {'✅ Passed' if status == 'success' else '❌ Failed'}
    Overall Pylint Score: {overall_score:.2f}/10

    Please review the detailed results on the platform.

    Best,
    The Code Review Team
    """
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")


def main():
    # Step 1: Set up the database
    setup_database()

    # Load the model
    tokenizer, model = load_model()

    # Fetch the GitHub token from environment variables
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

    # Check if the token is set
    if not GITHUB_TOKEN:
        raise ValueError("GITHUB_TOKEN environment variable is not set!")

    # Authenticate with GitHub
    g = Github(GITHUB_TOKEN)

    # Specify the repository
    REPO_NAME = "ReetikaNEU/AI_Code_Review"
    repo = g.get_repo(REPO_NAME)

    # Fetch open pull requests
    pulls = repo.get_pulls(state='open', sort='created', base='main')

    print(f"Open Pull Requests in {REPO_NAME}:")
    for pr in pulls:
        print(f"- PR #{pr.number}: {pr.title} by {pr.user.login}")

        # Fetch files changed in the pull request
        pylint_summary = ""
        pylint_scores = []
        for file in pr.get_files():
            print(f"- {file.filename}")

            # Run Pylint on the changed file
            print(f"Running Pylint on {file.filename}...")
            result = subprocess.run(
                ["pylint", file.filename],
                capture_output=True,
                text=True
            )

            # Extract Pylint score from the output
            pylint_output = result.stdout
            pylint_summary += f"\n### Pylint Report for {file.filename}:\n```\n{pylint_output}\n```\n"
            score = extract_pylint_score(pylint_output)
            if score is not None:
                pylint_scores.append(score)

            # AI Analysis
            try:
                with open(file.filename, "r") as f:
                    code_content = f.read()
                ai_results = analyze_code_with_ai(code_content, tokenizer, model)
                pylint_summary += f"\n### AI Analysis for {file.filename}:\n{ai_results}\n"
            except Exception as e:
                print(f"Error analyzing {file.filename} with AI: {e}")
                ai_results = "AI analysis failed."

            # Save results to the database
            save_results_to_database(pr.number, pr.title, pr.user.login, file.filename, score, ai_results)

        # Compute overall Pylint score
        overall_score = sum(pylint_scores) / len(pylint_scores) if pylint_scores else 0
        print(f"Overall Pylint Score for PR #{pr.number}: {overall_score}")

        # Determine success or failure
        status_state = "success" if overall_score >= 5.0 else "failure"
        status_description = f"Overall Pylint Score: {overall_score:.2f}/10"

        # Create a comment notifying the contributor
        notification_message = f"""
### Static Code Analysis Results
- **Overall Pylint Score**: {overall_score:.2f}/10
- **Status**: {"✅ Passed" if status_state == "success" else "❌ Failed"}

### Detailed Results:
{pylint_summary}

If you have questions or need help resolving the issues, please reach out!
        """
        pr.create_issue_comment(notification_message)
        print("Posted notification to the pull request.")

        # Create a GitHub status check
        create_status(repo, pr.head.sha, status_state, status_description)


if __name__ == "__main__":
    main()