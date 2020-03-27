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
         self.global_QQID_displayName={}
         self.__needAlert_userList={}#{'needAlertChannelID':{'member':['wang','x','b']},'needAlertChannelID':{'member':['wang','x','b']}}

    def getQQID(self,name,display_name):
        dict={'name':name,'display_name':display_name}
        try:
            dict['QQ'] = self.global_QQ_UserID[name]
            self.global_QQID_displayName[dict['QQ']] = display_name
        except:
            pass
        return dict
    
    @log
    def getUserList(self):        
        response = self.slack_web_client.users_list()
        print(response)
        if response['ok'] :
            for a in response['members']:
            #print(a['id'],a['name'])      
                self.global_userList[a['id']] = self.getQQID(a['name'],a['profile']['display_name'])

    @property
    def needAlert_userList(self):
        return self.__needAlert_userList
    
    def getchannelID_byName(self,name):
        for a in self.global_channels_List:
            if self.global_channels_List[a] == name:
                return a
        return ''

    @log
    def getchannelName(self,channelID):
        a= self.slack_web_client.conversations_info(channel=channelID)
        if a['ok']==False:
            return
        print(a)
        self.global_channels_List[a['channel']['id']] = a['channel']['name']
        
    @log
    def getchannelMembers(self,channelID):
        a = self.slack_web_client.conversations_members(channel=channelID)
        if a['ok'] ==False:
            return
        print(a)
        needlist=[]
        for userId in a['members']:
            if 'QQ' in self.global_userList[userId]:
                needlist.append(self.global_userList[userId]['QQ'])            
        if len(needlist)>0:
            self.__needAlert_userList[channelID]=needlist

    @log
    def getchannels_info(self,channelID):
        self.getchannelName(channelID)
        self.getchannelMembers(channelID)

    @log
    def getChannels_list(self):
        responsePrivate=self.slack_web_client.conversations_list(types='public_channel,private_channel')
        print(responsePrivate)
        for a in responsePrivate['channels']:
            self.global_channels_List[a['id']] = a['name']
            self.getchannels_info(a['id'])
      
        

    @log
    def get_group_member_list(self):    
        a = self.QQBot.get_group_member_list(group_id=config.group_id)
        for b in a:
            self.global_QQ_UserID[b['card']] =b['user_id']
    
    def findName_byQQId(self,QQId):
        if QQId in self.global_QQID_displayName:
            return self.global_QQID_displayName[QQId]
        return 'None'



    @log
    def autoloadaaa(self):
        try:
            if len(self.global_userList)==0:
                self.getUserList()
            if len(self.global_channels_List)==0:
                self.getChannels_list()
        except  Exception as inst:
            print(inst)
            pass



if __name__ == "__main__":
    slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
    prepareInfo =CPrePareInfo(slack_web_client,None)
    #prepareInfo.autoloadaaa()
    try:
        prepareInfo.getchannels_info('CUV4HHNSH')
    except  Exception as inst:
        print(inst)
    
