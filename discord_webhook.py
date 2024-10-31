
# import requests


# DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1301604054517944390/mIGquzAPJaZpiCoYaEc1299RMtiugJLnWXLNrSun7udO8nNQ50JwjwatTdcdlbQ3ka_Y'


# response = requests.post(DISCORD_WEBHOOK_URL, json={"content": "nothing"})

#  # Check for a successful response
# if response.status_code == 204:
#     print("Message sent to Discord successfully!")
# else:
#     print(f"Failed to send message to Discord: {response.status_code}, {response.text}")   
   
import os
import json
import requests

# Retrieve the Discord webhook URL and event data from environment variables
DISCORD_WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
event_data = os.environ.get('GITHUB_EVENT_DATA')

# Parse the JSON data
payload = json.loads(event_data)

# Determine the type of event
event_type = payload.get('action', 'push')  # Default to 'push' if action is not present

# Initialize message variable
message = None

# Handling Pull Request Events
if 'pull_request' in payload:
    action = payload.get('action')
    pull_request = payload.get('pull_request', {})
    pr_title = pull_request.get('title')
    pr_url = pull_request.get('html_url')
    pr_user = pull_request.get('user', {}).get('login')

    # Prepare message for Discord
    if action in ['opened', 'closed', 'reopened', 'edited']:
        message = f"Pull Request {action}:\n"
        message += f"**Title:** {pr_title}\n"
        message += f"**URL:** {pr_url}\n"
        message += f"**User:** {pr_user}\n"

# Handling Push Events
elif 'commits' in payload:
    pusher = payload.get('pusher', {}).get('name')
    commits = payload.get('commits', [])
    commit_messages = [commit['message'] for commit in commits]

    # Prepare message for Discord
    message = f"New Push by {pusher}:\n"
    message += "\n".join(commit_messages)  # Join commit messages into a single string

# Send the message to Discord if there's a valid message to send
if message:
    response = requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
    
    # Check for a successful response
    if response.status_code == 204:
        print("Message sent to Discord successfully!")
    else:
        print(f"Failed to send message to Discord: {response.status_code}, {response.text}")
