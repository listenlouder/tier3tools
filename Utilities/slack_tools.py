import json
from slackclient import SlackClient
# Currently doesn't do anything since slack tokens are disabled :(
json_info = json.load(open('Resources/slack.json'))

try:
    token = json_info['token']
    sc = SlackClient(token)
except KeyError:
    print "Slack auth not found. Check help.txt for more info."
    exit()


def send_message(room, from_name, content):
    sc.api_call("chat.postMessage", channel=room, username=from_name, text=content)