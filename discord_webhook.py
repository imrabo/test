
import os
import json
import requests

# Retrieve the Discord webhook URL and event data from environment variables
# DISCORD_WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1301604054517944390/mIGquzAPJaZpiCoYaEc1299RMtiugJLnWXLNrSun7udO8nNQ50JwjwatTdcdlbQ3ka_Y'

# Set Discord webhook URL
# DISCORD_WEBHOOK_URL = os.environ.get('WEBHOOK_URL', 'https://discord.com/api/webhooks/...')  # Replace with your webhook URL or keep it secure with an env variable

# Retrieve GitHub event data
event_data = os.environ.get('GITHUB_EVENT_DATA')
if not event_data:
    raise ValueError("GitHub event data is not available")

# Parse the JSON data
payload = json.loads(event_data)

# Determine the event type
event_type = payload.get('action', 'push')  # Defaults to 'push' if 'action' is missing

# Initialize message variable
message = None

# Handle Pull Request Events
if 'pull_request' in payload:
    action = payload.get('action')
    pull_request = payload['pull_request']
    pr_title = pull_request.get('title')
    pr_url = pull_request.get('html_url')
    pr_user = pull_request['user']['login']
    pr_body = pull_request.get('body', '')

    if action in ['opened', 'closed', 'reopened', 'edited']:
        message = (
            f"Pull Request {action.capitalize()}:\n"
            f"**Title:** {pr_title}\n"
            f"**Description:** {pr_body}\n"
            f"**User:** {pr_user}\n"
            f"**URL:** {pr_url}"
        )

# Handle Push Events
elif 'commits' in payload:
    pusher = payload['pusher']['name']
    ref = payload.get('ref', 'unknown branch')
    commits = payload['commits']
    commit_messages = [f"- {commit['message']}" for commit in commits]
    commit_count = len(commit_messages)

    message = (
        f"New Push to `{ref}` by {pusher}:\n"
        f"**{commit_count} Commit(s):**\n" +
        "\n".join(commit_messages)
    )

# Handle Issues Events
elif 'issue' in payload:
    action = payload['action']
    issue = payload['issue']
    issue_title = issue.get('title')
    issue_url = issue.get('html_url')
    issue_user = issue['user']['login']
    issue_body = issue.get('body', '')

    if action in ['opened', 'closed', 'reopened', 'edited']:
        message = (
            f"Issue {action.capitalize()}:\n"
            f"**Title:** {issue_title}\n"
            f"**Description:** {issue_body}\n"
            f"**User:** {issue_user}\n"
            f"**URL:** {issue_url}"
        )

# Handle Issue Comment Events
elif 'comment' in payload:
    action = payload['action']
    comment = payload['comment']
    comment_body = comment.get('body')
    comment_url = comment.get('html_url')
    issue = payload.get('issue', {})
    issue_title = issue.get('title', 'N/A')
    comment_user = comment['user']['login']

    if action in ['created', 'edited', 'deleted']:
        message = (
            f"Comment {action.capitalize()} on Issue: {issue_title}\n"
            f"**Comment:** {comment_body}\n"
            f"**User:** {comment_user}\n"
            f"**URL:** {comment_url}"
        )

# Add more event types as needed...

# Send the message to Discord if there's a valid message to send
if message:
    response = requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
    
    # Check for a successful response
    if response.status_code == 204:
        print("Message sent to Discord successfully!")
    else:
        print(f"Failed to send message to Discord: {response.status_code}, {response.text}")
else:
    print("No recognized action or message to send.")
