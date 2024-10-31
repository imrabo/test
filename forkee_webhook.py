import os
import json
import requests

# Set Discord webhook URL (best to set this as an environment variable)
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1301604054517944390/mIGquzAPJaZpiCoYaEc1299RMtiugJLnWXLNrSun7udO8nNQ50JwjwatTdcdlbQ3ka_Y'

# Retrieve GitHub event data from the environment variable
event_data = os.environ.get('GITHUB_EVENT_DATA')
if not event_data:
    raise ValueError("GitHub event data is not available")

# Parse the JSON data
payload = json.loads(event_data)

# Initialize the message variable
message = None

# Handle Fork Event
if 'forkee' in payload:
    forked_repo = payload['forkee']
    repo_name = forked_repo.get('full_name')
    fork_owner = forked_repo['owner']['login']
    fork_url = forked_repo.get('html_url')
    parent_repo = payload['repository'].get('full_name')

    message = (
        f"🔀 **Repository Forked**:\n"
        f"**Parent Repository:** {parent_repo}\n"
        f"**Forked By:** {fork_owner}\n"
        f"**New Repository:** [{repo_name}]({fork_url})\n"
        f"Visit the forked repo here: {fork_url}"
    )

# Send the message to Discord if there's a valid message to send
if message:
    response = requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
    
    # Check for a successful response
    if response.status_code == 204:
        print("Fork event notification sent to Discord successfully!")
    else:
        print(f"Failed to send notification to Discord: {response.status_code}, {response.text}")
else:
    print("No fork event detected in payload.")
