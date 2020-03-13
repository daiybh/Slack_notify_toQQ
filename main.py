#Using your existing Flask instance:

from flask import Flask,redirect,render_template
from slackeventsapi import SlackEventAdapter
from cqhttp import CQHttp
from slack import WebClient
import json
import os,sys,threading
# This `app` represents your existing Flask app

import config
import  prepareInfo
import asyncio

app = Flask(__name__,static_url_path='')

bot = CQHttp(config.api_root, config.access_token, config.secret,server=app)

def get_group_member_list():    
    a = bot.get_group_member_list(group_id=config.group_id)
    for b in a:
        prepareInfo.global_QQ_UserID[b['card']] =b['user_id']
    

get_group_member_list()



slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
slack_events_adapter = SlackEventAdapter(os.environ["SLACK_SIGNING_SECRET"], "/slack/events", app)


lastEventTS=0.0
lock=threading.Lock()

@bot.on_message
def handle_msg(event):
    bot.send(event, 'not supported')
    slack_web_client.chat_postMessage(channel='CV8PBFSKE',text=str(event['message']))
    #return {'reply': event['message'], 'at_sender': False}


@app.route('/')
def aaaa():
  print(app.url_map)
  #return str(app.url_map)
  return render_template('index.html')

  
@app.route('/a')
def index():    
    prepareInfo.autoload()   
    
    print(prepareInfo.global_userList)
    print(prepareInfo.global_channels_List)
    print(prepareInfo.global_QQ_UserID)
    print(prepareInfo.needAlert_userList)
    
    return render_template('index.html'
    ,lastEventTS=lastEventTS
    ,userlist=prepareInfo.global_userList 
    ,global_channels_List=prepareInfo.global_channels_List
    ,global_QQ_UserID=prepareInfo.global_QQ_UserID
    ,needAlert_userList=prepareInfo.needAlert_userList)




@app.route("/oauth")
def oauth():
    return redirect("http://slack.com/oauth/authorize", code=302)


@slack_events_adapter.on("app_mention")
def app_mentionA(event_data):
    print("app_mention",event_data,event_data['token'])
    bot.send_group_msg(group_id=config.group_id, message='slack mention you msg')

def replaceUser(text):
    bLast=False
    Msg=''
    try:
      for a in text.split('@'):
          if bLast :
              end = a.find('>')
              if end >-1:
                  a='@'+ prepareInfo.global_userList[a[:end]]+a[end:]['name']
          Msg =Msg +a
          bLast =  a[-1] =='<'
    except:
      return text
    if Msg=='':
      return text
    return Msg

def makeMsg(event_data):
    text = event_data['event']['text']
    return  '#'+ prepareInfo.global_channels_List[event_data['event']['channel']]+' '+ prepareInfo.global_userList[event_data['event']['user']]['name']+" say: "+replaceUser(text)


def transferMessage(event_data):  
    message=makeMsg(event_data)
    if event_data['event']['channel'] not in prepareInfo.needAlert_userList:
        bot.send_group_msg(group_id=config.group_id, message=message)
        return
    
    for a in prepareInfo.needAlert_userList[event_data['event']['channel']]:        
        bot.send_private_msg(user_id=a, message=message)


@slack_events_adapter.on("message")
def handle_message(event_data):
    print(event_data)
    global lastEventTS,lock
    with lock:    
      
      prepareInfo.autoload()
      if lastEventTS < event_data['event_time']:
        lastEventTS = event_data['event_time']
        transferMessage(event_data)
          

@app.route('/pp')
def route_pp():
     return str(bot.send_private_msg(user_id=7277017, message='message'))       
          
# Start the server on port 3000
if __name__ == "__main__":
  #prepareInfo.autoload()
  if len(sys.argv)>1:
    app.run(port=3443,ssl_context='adhoc')
  else:
    app.run(port=3000)
