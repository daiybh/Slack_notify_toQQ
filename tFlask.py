from flask import Flask,redirect,render_template
import prepareInfo
app = Flask(__name__,static_url_path='')



@app.route('/')
def aaaa():
    if len(prepareInfo.global_userList)==0:
      prepareInfo.autoload()
    
    
    print(prepareInfo.global_userList)
    print(prepareInfo.global_channels_List)
    print(prepareInfo.global_QQ_UserID)
    print(prepareInfo.needAlert_userList)
    
    return render_template('hh.html'
    ,userlist=prepareInfo.global_userList 
    ,global_channels_List=prepareInfo.global_channels_List
    ,global_QQ_UserID=prepareInfo.global_QQ_UserID
    ,needAlert_userList=prepareInfo.needAlert_userList)


  
          
# Start the server on port 3000
if __name__ == "__main__":  
    app.run(port=3000)
