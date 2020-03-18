from flask import Flask, request, make_response, Response
import os
import json

import config
from slack import WebClient


import json

aJson='{"name":"games_list","value":"","callback_id":"menu_options_2319","type":"interactive_message","team":{"id":"TRES3JDRU","domain":"websimplylivetv"},"channel":{"id":"CV8PBFSKE","name":"test_bot"},"user":{"id":"UUKJZPB8Q","name":"d.li"},"action_ts":"1584344644.363215","message_ts":"1584333129.016500","attachment_id":"1","token":"5D2oixB0s3TnuOHu0f37okkH"}'

bbbb = json.loads(aJson)

# Your app's Slack bot user token

# Slack client for Web API requests

# Flask webserver for incoming traffic from Slack

# Send a Slack message on load. This needs to be _before_ the Flask server is started

# A Dictionary of message attachment options
attachments_json = [
    {
        "fallback": "Upgrade your Slack client to use messages like these.",
        "color": "#3AA3E3",
        "attachment_type": "default",
        "callback_id": "menu_options_2319",
        "actions": [
            {
                "name": "bev_list",
                "text": "Pick a beverage...",
                "type": "select",
                "data_source": "external"
            }
        ]
    }
]

message_attachments = [
    {
        "fallback": "Upgrade your Slack client to use messages like these.",
        "color": "#3AA3E3",
        "attachment_type": "default",
        "callback_id": "menu_options_2319",
        "actions": [
            {
                "name": "games_list",
                "text": "Pick a game...",
                "type": "select",
                "data_source": "external"
            }
        ]
    }
]
slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

a =slack_web_client.chat_postMessage(channel='CV8PBFSKE',
text="Shall we play a game111111?",
    attachments=message_attachments)
print(a)


slack_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
try:
    

    rr = slack_client.chat_postMessage(channel='CV8PBFSKE',
    text="Shall we play a game?",
    attachments=message_attachments)

    print(rr)
except :
    print('lllll 11111')
    

try:
    # Send a message with the above attachment, asking the user if they want coffee
    a = slack_client.chat_postMessage(
    channel="CV8PBFSKE",
    text="Would you like some coffee? :coffee:",
    attachments=attachments_json
    )
    print(a)
except:
    
    print('lllll 222222')




