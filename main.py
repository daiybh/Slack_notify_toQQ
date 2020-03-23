#Using your existing Flask instance:

from flask import Flask,redirect,render_template,request,Response,make_response
from slackeventsapi import SlackEventAdapter
from cqhttp import CQHttp
from slack import WebClient
import json,datetime
import os,sys,threading
import requests
# This `app` represents your existing Flask app

import config
from  prepareInfo import CPrePareInfo
import asyncio


lastRecvedChannels={}

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_VERIFICATION_TOKEN = os.environ["SLACK_VERIFICATION_TOKEN"]


app = Flask(__name__,static_url_path='')

bot = CQHttp(config.api_root, config.access_token, config.secret,server=app)
slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
slack_events_adapter = SlackEventAdapter(os.environ["SLACK_SIGNING_SECRET"], "/slack/events", app)


prepareInfo =CPrePareInfo(slack_web_client,bot)

prepareInfo.get_group_member_list()
prepareInfo.getUserList()


lastEventTS=0.0
lock=threading.Lock()

@bot.on_message
def handle_msg(event):
    #bot.send(event, 'not supported')
    channel=''
    msg = event['message']
   # print('msg',msg,'----->',msg[0])
    if msg[0]=='#':
    #  print("msg######")
      sa = msg.find(' ')
     # print(sa)
      if sa>1:
        channel= prepareInfo.getchannelID_byName(msg[1:sa])
      #  print('channle',msg[1:sa],channel)
        if channel!="":
          msg = msg[sa:]
   # print('channel2',channel)
    if channel=='' :
      if event['user_id'] in lastRecvedChannels:
        channel=lastRecvedChannels[event['user_id']]      
      else:
        return ' '

    slack_web_client.chat_postMessage(channel=channel,text=prepareInfo.findName_byQQId(event['user_id']) +"   say: "+str(msg))
    

    print("bot.on_message  handlemsg-->",event['message'] ,event['user_id'],channel)
    return '' #{'reply': event['message'], 'at_sender': False}


@app.route('/')
def aaaa():
  ip = requests.get('http://myip.ipip.net/')
  return render_template('index.html',cc=str(app.url_map),time=datetime.datetime.now(),ip=ip.text)

#CV8PBFSKE
@app.route('/a/<name>')  
@app.route('/a')
def index(name=''):    
    #prepareInfo.autoload()   
    ip = requests.get('http://myip.ipip.net/')
    
    #print(prepareInfo.global_userList)
    #print(prepareInfo.global_channels_List)
    #print(prepareInfo.global_QQ_UserID)
    #print(prepareInfo.needAlert_userList)
    if name!='' and name not in prepareInfo.needAlert_userList:
      print("name not in",name)
      prepareInfo.getchannels_info(name)
      
      name = name +" not in  prepareInfo.needAlert_userList"
      
    return render_template('index.html'
    ,lastEventTS=lastEventTS
    ,userlist=prepareInfo.global_userList 
    ,global_channels_List=prepareInfo.global_channels_List
    ,global_QQ_UserID=prepareInfo.global_QQ_UserID
    ,needAlert_userList=prepareInfo.needAlert_userList
    ,time=datetime.datetime.now()
    ,name=name
    ,ip=ip.text)




@app.route("/oauth")
def oauth():
    return redirect("http://slack.com/oauth/authorize", code=302)


# Helper for verifying that requests came from Slack
def verify_slack_token(request_token):
    if SLACK_VERIFICATION_TOKEN != request_token:
        print("Error: invalid verification token!")
        print("Received {} but was expecting {}".format(request_token, SLACK_VERIFICATION_TOKEN))
        return make_response("Request contains invalid Slack verification token", 403)



# The endpoint Slack will load your menu options from
@app.route("/slack/message_options", methods=["POST"])
def message_options():
    # Parse the request payload
    print("message_options post")
    form_json = json.loads(request.form["payload"])

    # Verify that the request came from Slack
    verify_slack_token(form_json["token"])

    # Dictionary of menu options which will be sent as JSON
    menu_options = {
        "options": [
            {
                "text": "Cappuccino",
                "value": "cappuccino"
            },
            {
                "text": "Latte",
                "value": "latte"
            }
        ]
    }

    # Load options dict as JSON and respond to Slack
    return Response(json.dumps(menu_options), mimetype='application/json')


# The endpoint Slack will send the user's menu selection to
@app.route("/slack/message_actions", methods=["POST"])
def message_actions():

    # Parse the request payload
    form_json = json.loads(request.form["payload"])

    # Verify that the request came from Slack
    verify_slack_token(form_json["token"])

    # Check to see what the user's selection was and update the message accordingly
    selection = form_json["actions"][0]["selected_options"][0]["value"]

    if selection == "cappuccino":
        message_text = "cappuccino"
    else:
        message_text = "latte"

    response = slack_web_client.chat_update(
      channel=form_json["channel"]["id"],
      ts=form_json["message_ts"],
      text="One {}, right coming up! :coffee:".format(message_text),
      attachments=[] # empty `attachments` to clear the existing massage attachments
    )

    # Send an HTTP 200 response with empty body so Slack knows we're done here
    return make_response("", 200)



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
                print('aaaa->',a[:end],"------",a[end:])
                a='@'+ prepareInfo.global_userList[a[:end]]['name']+a[end:]
          Msg =Msg +a
          bLast =  a[-1] =='<'
    except:
      return text
    if Msg=='':
      return text
    return Msg

def makeMsg(event_data):
    text = event_data['event']['text']
    try:
      if event_data['event']['channel'] not in prepareInfo.global_channels_List:
        prepareInfo.getchannels_info(event_data['event']['channel'])
      return  '#'+ prepareInfo.global_channels_List[event_data['event']['channel']]+' '+ prepareInfo.global_userList[event_data['event']['user']]['name']+" say: "+replaceUser(text)
    except:
      return text

def transferMessage(event_data):  
    message=makeMsg(event_data)
    if event_data['event']['channel'] not in prepareInfo.needAlert_userList:
        bot.send_group_msg(group_id=config.group_id, message=message)
        return
    
    for a in prepareInfo.needAlert_userList[event_data['event']['channel']]:        
        bot.send_private_msg(user_id=a, message=message)
        lastRecvedChannels[a] = event_data['event']['channel']


@slack_events_adapter.on("message")
def handle_message(event_data):
    print(event_data)
    global lastEventTS,lock
    with lock:      
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
