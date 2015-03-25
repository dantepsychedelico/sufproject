
import json, time

from Users import Users
from mongoCtrl import mongoCtrl as mctrl

class router:
    def __init__(self, socket):
        self.socket = socket
        self.uid = None
        self.__route = {
                "new": self.newUser, 
                "online": self.updateSocket
                }

    def Ctrl(self, reqBinary):
        data = json.loads(reqBinary.decode())
        method = data["method"]
        if self.uid is None:
            self.uid = data.get("uid")
        res = self.__route[method](data)
        res["method"] = method
        res["status"] = "ok"
        return json.dumps(res).encode()

    def newUser(self, data):
        ## uid: user id
        ## sid: security id
        self.uid = Users.createUser(self.socket)
        self.sid = int(time.time())
        mctrl.signUp(self.uid, self.sid)
        return {"uid": self.uid, "sid": hex(self.sid)[2:]}

    def updateSocket(self, data):
        self.uid = data["uid"]
        Users.updateSocket(self.uid, self.socket)
        return {"uid": self.uid}

    def stopSocket(self):
        Users.removeSocket(self.uid)

    def newRoom(self, data):
        roomid, createtime = mctrl.newRoom(**data)
        return {"roomid": roomid, "createtime": createtime}

    def joinRoom(self, data):
        return 

    def chat(self, data):
        return

