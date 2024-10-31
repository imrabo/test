
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
import sys

# Retrieve the Discord webhook URL from environment variables
DISCORD_WEBHOOK_URL = os.environ.get('WEBHOOK_URL')

# Read the payload from standard input (GitHub Action passes it as input)
payload = json.loads(sys.stdin.read())

# Extract relevant information from the payload
action = payload.get('action')
pull_request = payload.get('pull_request', {})
pr_title = pull_request.get('title')
pr_url = pull_request.get('html_url')
pr_user = pull_request.get('user', {}).get('login')

# Prepare the message for Discord
if action in ['opened', 'closed', 'reopened', 'edited']:
    message = f"Pull Request {action}:\n"
    message += f"**Title:** {pr_title}\n"
    message += f"**URL:** {pr_url}\n"
    message += f"**User:** {pr_user}\n"
    
    # Send the message to Discord
    response = requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
    
    # Check for a successful response
    if response.status_code == 204:
        print("Message sent to Discord successfully!")
    else:
        print(f"Failed to send message to Discord: {response.status_code}, {response.text}")
