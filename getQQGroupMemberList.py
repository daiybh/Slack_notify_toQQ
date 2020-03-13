
import requests
import json
def get_group_member_list(api_root,group_id):    
    global_QQ_UserID={}
    url=api_root +'get_group_member_list'
    a = requests.get(url,params={'group_id':group_id})
    print(a.url)
    for b in a.json()['data']:
        global_QQ_UserID[b['card']] =b['user_id']
    return global_QQ_UserID


def sendPrivateMesage(api_root,user_id,message):
    #http://118.24.49.134:5700/send_private_msg?user_id=2914499&message=hello
    url=api_root +'send_private_msg'
    a = requests.get(url,params={'user_id':user_id,'message':message})    
    return a.text
