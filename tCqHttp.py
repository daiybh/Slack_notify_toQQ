from cqhttp import CQHttp
import config,os
from flask import Flask,redirect,render_template
import requests
from slackeventsapi import SlackEventAdapter

app = Flask("llll")
bot = CQHttp(config.api_root, config.access_token, config.secret,server=app)

app = bot.server_app
@bot.on_message

def handle_msg(event):
    bot.send(event, '你好呀，下面一条是你刚刚发的：')
    return {'reply': event['message'], 'at_sender': False}


@bot.on_notice('group_increase')  # 如果插件版本是 3.x，这里需要使用 @bot.on_event
def handle_group_increase(event):
    bot.send(event, message='欢迎新人～', auto_escape=True)  # 发送欢迎新人


@bot.on_request('group', 'friend')
def handle_request(event):
    return {'approve': True}  # 同意所有加群、加好友请求

@app.route("/")
def oauth():
    
    #bot.send_private_msg(user_id=7277017, message='hello')
    return 'hhhhh'

slack_events_adapter = SlackEventAdapter(os.environ["SLACK_SIGNING_SECRET"], "/slack/events", bot.server_app)


app.run(host='127.0.0.1', port=8080)
