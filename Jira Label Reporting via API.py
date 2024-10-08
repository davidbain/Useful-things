import requests
from collections import Counter
import csv
 
'''
Script that uses the Jira API to evaluate labels applied to tickets and count each occurance. Used for basic reporting.
Outputs report to CSV.
Adjust settings below as needed.
'''
 
# SETTINGS
# Add your API token details here - https://id.atlassian.com/manage-profile/security/api-tokens
JIRA_URL = 'https://YOURSITE.atlassian.net'
USERNAME = 'email@example.com'
API_TOKEN = 'YOURTOKEN'
# Set reporting timeframe in days
TIMEFRAME = "365"
# File path for saving the CSV file - be use to double backslash as the escape character e.g. C:\\folder\\anotherfolder\\filename.csv
CSV_PATH = "C:\\temp\\Jira labels report.csv"
# STOP EDITING HERE
 
# API endpoint to search for issues
SEARCH_URL = f'{JIRA_URL}/rest/api/3/search'
 
# Build JQL query for a specific time range (e.g., last N days)
def build_jql_query(days_ago):
    return f'created >= -{days_ago}d AND labels IS NOT EMPTY'
 
 
# Set up authentication and headers
auth = (USERNAME, API_TOKEN)
headers = {
    'Accept': 'application/json'
}
 
 
# Fetch issues from Jira
def fetch_issues(jql, start_at=0, max_results=50):
    params = {
        'jql': jql,
        'fields': 'labels',
        'startAt': start_at,
        'maxResults': max_results
    }
    response = requests.get(SEARCH_URL, headers=headers, auth=auth, params=params)
    response.raise_for_status()
    return response.json()
 
 
# Count labels across all tickets for the given JQL query
def count_labels(days_ago):
    jql = build_jql_query(days_ago)
    labels_counter = Counter()
    start_at = 0
    max_results = 50
    total = None
 
    # Loop to handle Jira 100 item limit
    while total is None or start_at < total:
        # Fetch a batch of issues
        data = fetch_issues(jql, start_at, max_results)
       
        # Update total issues count
        if total is None:
            total = data['total']
       
        # Count labels in the fetched issues
        for issue in data['issues']:
            labels = issue['fields'].get('labels', [])
            labels_counter.update(labels)
       
        start_at += max_results
 
    return labels_counter
 
 
# Create a CSV of results
def create_csv_report(label_counts, days_ago):
   
    with open(CSV_PATH, mode='w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
       
        # Write the header
        csv_writer.writerow(["Label", "Count"])
       
        # Write the label counts
        for label, count in sorted(label_counts.items(), key=lambda x: x[1], reverse=True):
            csv_writer.writerow([label, count])
 
    print(f"CSV report generated: {CSV_PATH}")
 
 
# Run
if __name__ == "__main__":
 
    label_counts = count_labels(TIMEFRAME)
 
    # Order results descending
    sorted_label_counts = sorted(label_counts.items(), key=lambda x: x[1], reverse=True)
 
    create_csv_report(label_counts, TIMEFRAME)
