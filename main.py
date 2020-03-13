#Using your existing Flask instance:

from flask import Flask,redirect
from slackeventsapi import SlackEventAdapter
from cqhttp import CQHttp
from slack import WebClient
import json
import os,sys,threading
# This `app` represents your existing Flask app
app = Flask(__name__)
import config

bot = CQHttp(config.api_root, config.access_token, config.secret)
slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
global_userList={}
global_channels_List={}

lastEventTS=0.0
lock=threading.Lock()

def getUserList():
  response = slack_web_client.users_list()
  if response['ok'] :
    for a in response['members']:
      print(a['id'],a['name'])
      global_userList[a['id']] = a['name']


def getChannels_list():
    response = slack_web_client.channels_list()
    for a in response['channels']:
        global_channels_List[a['id']] = a['name']
        

getUserList()
getChannels_list()

# An example of one of your Flask app's routes
@app.route("/")
def hello():
  xhtml=str(lastEventTS)+"\n"
  for a in global_channels_List:
      xhtml=xhtml+"<li>"+a+"   "+global_channels_List[a]+"</li>"
  xhtml=xhtml+"<br>"
  for a in global_userList:
      xhtml=xhtml+"<li>"+a+"   "+global_userList[a]+"</li>"

  return "Hello there!\n"+xhtml


@app.route("/oauth")
def oauth():
    return redirect("http://slack.com/oauth/authorize", code=302)


# Bind the Events API route to your existing Flask app by passing the server
# instance as the last param, or with `server=app`.
slack_events_adapter = SlackEventAdapter(os.environ["SLACK_SIGNING_SECRET"], "/slack/events", app)


# Create an event listener for "reaction_added" events and print the emoji name
@slack_events_adapter.on("reaction_added")
def reaction_added(event_data):
  emoji = event_data["event"]["reaction"]
  print(emoji)

@slack_events_adapter.on("message.channel")
def messageChat(event_data):
    print("messagechannels")

@slack_events_adapter.on("app_mention")
def app_mentionA(event_data):
    print("app_mention",event_data,event_data['token'])
    bot.send_group_msg(group_id=config.group_id, message='slack mention you msg')

def replaceUser(text):

    bLast=False
    Msg=''
    for a in text.split('@'):
        if bLast :
            end = a.find('>')
            if end >-1:
                a='@'+ global_userList[a[:end]]+a[end:]
        Msg =Msg +a
        bLast =  a[-1] =='<'
    if Msg=='':
      return text
    return Msg

def makeMsg(event_data):
    text = event_data['event']['text']
    return  '#'+ global_channels_List[event_data['event']['channel']]+' '+ global_userList[event_data['event']['user']]+" say: "+replaceUser(text)


@slack_events_adapter.on("message")
def handle_message(event_data):
    print(event_data)
    global lastEventTS,lock
    with lock:
       if lastEventTS < event_data['event_time']:
          lastEventTS = event_data['event_time']
          bot.send_group_msg(group_id=config.group_id, message=makeMsg(event_data))
# Start the server on port 3000
if __name__ == "__main__":
  if len(sys.argv)>1:
    app.run(port=3443,ssl_context='adhoc')
  else:
    app.run(port=3000)
