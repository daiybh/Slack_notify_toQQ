





import datetime
import time

class TailMsg:
    def __init__(self):
        self.updateDay= datetime.datetime.now()
        self.destDay  = datetime.datetime(1980,12,2,0,0,0)
        self.destDay= self.destDay.replace(self.updateDay.year)
        self.leftDay = self.destDay.__sub__(datetime.datetime.now())
    
    def getMsg(self):
        
        self.leftDay = self.destDay.__sub__(datetime.datetime.now())
        
        msg="\n left--->{}".format(self.leftDay)
        return msg

class Tailer:
    def __init__(self):
        self.lastUPdate=datetime.datetime.now()
        self.updateCount=0
    
    def addTailer(self):
        a = datetime.datetime.now()
        diff = a-self.lastUPdate
        if diff > datetime.timedelta(hours=1):
            self.updateCount=0
            self.lastUPdate = a

        self.updateCount+=1
        return self.updateCount<10
        



tmsg = TailMsg()
tailist={}

def addTail(userid,message):
    
    if userid not in tailist:
      tailist[userid]=Tailer()

    if tailist[userid].addTailer():
        message=message+tmsg.getMsg()
    
    return message



if __name__ == "__main__":
    for i in range(12):
        print(addTail("a","aaaaaa"+str(i)))
    print(addTail("a","aaaaaa"))


