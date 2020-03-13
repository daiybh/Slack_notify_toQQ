import config

import os

from slack import WebClient
import getQQGroupMemberList

slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

global_userList={}
global_channels_List={}
global_QQ_UserID={}
needAlert_userList={}#{'needAlertChannelID':{'member':['wang','x','b']},'needAlertChannelID':{'member':['wang','x','b']}}


def getQQID(name):
    dict={'name':name}
    try:
        dict['QQ'] = global_QQ_UserID[name]
    except:
        pass
    return dict
def getUserList():
  response = slack_web_client.users_list()
  #print(response)
  if response['ok'] :
    for a in response['members']:
      #print(a['id'],a['name'])      
      global_userList[a['id']] = getQQID(a['name'])



def getchannels_info(channelID):
    a = slack_web_client.channels_info(channel=channelID)    
    needlist=[]
    for userId in a['channel']['members']:
        if 'QQ' in global_userList[userId]:
            needlist.append(global_userList[userId]['QQ'])            
    if len(needlist)>0:
        needAlert_userList[channelID]=needlist

def getChannels_list():
    response = slack_web_client.channels_list()
    #print(response)
    for a in response['channels']:
        global_channels_List[a['id']] = a['name']
        getchannels_info(a['id'])

def autoload():
    try:
        global global_QQ_UserID
        global_QQ_UserID=getQQGroupMemberList.get_group_member_list(config.api_root,config.group_id)

        getUserList()
        getChannels_list()
    except:
        pass

    for a in needAlert_userList:
        print(a)