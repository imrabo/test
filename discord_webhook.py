import os
import json
import requests
from flask import Flask, request

app = Flask(__name__)

DISCORD_WEBHOOK_URL = os.environ.get('WEBHOOK_URL')  # Set this in your GitHub Secrets

@app.route('/github-webhook', methods=['POST'])
def github_webhook():
    data = request.json
    action = data.get('action')
    pull_request = data.get('pull_request', {})
    pr_title = pull_request.get('title')
    pr_url = pull_request.get('html_url')
    pr_user = pull_request.get('user', {}).get('login')
    
    # Prepare message for Discord
    if action in ['opened', 'closed', 'reopened', 'edited']:
        message = f"Pull Request {action}:\n"
        message += f"**Title:** {pr_title}\n"
        message += f"**URL:** {pr_url}\n"
        message += f"**User:** {pr_user}\n"
        
        # Send message to Discord
        requests.post(DISCORD_WEBHOOK_URL, json={"content": message})

    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
