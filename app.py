from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def fetch_results(pr_id=None, author=None, sort_by="timestamp"):
    """Fetch historical analysis results from the database with optional filters and sorting."""
    conn = sqlite3.connect("code_analysis.db")  # Connect to the database
    cursor = conn.cursor()

    # Build the base query
    query = """
        SELECT 
            id, 
            pull_request_id, 
            title, 
            author, 
            file_name, 
            pylint_score, 
            ai_analysis, 
            timestamp 
        FROM pull_request_analysis
        WHERE 1=1
    """

    # Add filters dynamically
    params = []
    if pr_id:
        query += " AND pull_request_id = ?"
        params.append(pr_id)
    if author:
        query += " AND author LIKE ?"
        params.append(f"%{author}%")

    # Add sorting
    if sort_by in ["pylint_score", "timestamp"]:
        query += f" ORDER BY {sort_by} DESC"
    else:
        query += " ORDER BY timestamp DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows


@app.route("/")
def index():
    """Homepage that displays historical results with optional filtering."""
    pr_id = request.args.get("pr_id")  # Get the Pull Request ID from the URL parameters
    author = request.args.get("author")  # Get the author filter from the URL parameters
    sort_by = request.args.get("sort_by", "timestamp")  # Get the sorting option from the URL parameters
    results = fetch_results(pr_id=pr_id, author=author, sort_by=sort_by)
    return render_template("index.html", results=results, pr_id=pr_id, author=author, sort_by=sort_by)


if __name__ == "__main__":
    app.run(debug=True)