import os
import slack
import config
client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'])
response = client.api_call(
    api_method='chat.postMessage',
    json={'channel': '#test_bot','text': "Hello world!"}
)

print(response)