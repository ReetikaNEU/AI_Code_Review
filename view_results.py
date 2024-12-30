import sqlite3
from tabulate import tabulate  # For pretty-printing tables (install with `pip install tabulate`)

def fetch_results():
    """Fetch historical analysis results from the database."""
    conn = sqlite3.connect("code_analysis.db")  # Connect to the database
    cursor = conn.cursor()

    # Query to fetch all records
    cursor.execute("""
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
        ORDER BY timestamp DESC
    """)

    # Fetch all results
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    return rows


def display_results(rows):
    """Display analysis results in a table format."""
    if not rows:
        print("No historical data found in the database.")
        return

    # Define table headers
    headers = ["ID", "PR ID", "Title", "Author", "File Name", "Pylint Score", "AI Analysis", "Timestamp"]

    # Use tabulate to print the results
    print(tabulate(rows, headers=headers, tablefmt="pretty"))


if __name__ == "__main__":
    print("Fetching historical analysis results...")
    results = fetch_results()
    display_results(results)