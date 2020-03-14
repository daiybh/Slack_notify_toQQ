import config

import os,time

from slack import WebClient

def log(func):
    def wrapper(*args, **kw):
        start = time.time()
        run_func= func(*args, **kw)
        end = time.time()
        print('%s executed in %s ms' % (func.__name__, (end - start) * 1000))
        return run_func
    return wrapper

class CPrePareInfo:
    def __init__(self,slack_web_client,QQBot):
         self.slack_web_client = slack_web_client
         self.QQBot = QQBot
         
         self.global_userList={}
         self.global_channels_List={}
         self.global_QQ_UserID={}
         self.__needAlert_userList={}#{'needAlertChannelID':{'member':['wang','x','b']},'needAlertChannelID':{'member':['wang','x','b']}}

    def getQQID(self,name):
        dict={'name':name}
        try:
            dict['QQ'] = self.global_QQ_UserID[name]
        except:
            pass
        return dict
    
    @log
    def getUserList(self):        
        response = self.slack_web_client.users_list()
        #print(response)
        if response['ok'] :
            for a in response['members']:
            #print(a['id'],a['name'])      
                self.global_userList[a['id']] = self.getQQID(a['name'])

    @property
    def needAlert_userList(self):
        return self.__needAlert_userList
    
    @log
    def getchannels_info(self,channelID):
        a = self.slack_web_client.channels_info(channel=channelID)    
        
        if a['ok'] ==False:
            return
        needlist=[]
        self.global_channels_List[a['channel']['id']] = a['channel']['name']
        for userId in a['channel']['members']:
            if 'QQ' in self.global_userList[userId]:
                needlist.append(self.global_userList[userId]['QQ'])            
        if len(needlist)>0:
            self.__needAlert_userList[channelID]=needlist

    @log
    def getChannels_list(self):
        response = self.slack_web_client.channels_list()
        #print(response)
        for a in response['channels']:
            self.global_channels_List[a['id']] = a['name']
            self.getchannels_info(a['id'])

    @log
    def get_group_member_list(self):    
        a = self.QQBot.get_group_member_list(group_id=config.group_id)
        for b in a:
            self.global_QQ_UserID[b['card']] =b['user_id']
    



    @log
    def autoload(self):
        try:
            if len(self.global_userList)==0:
                self.getUserList()
            if len(self.global_channels_List)==0:
                self.getChannels_list()
        except:
            pass
