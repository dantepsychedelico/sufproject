
import json, time

from Users import users
from mongoCtrl import mongoCtrl as mctrl

class router:
    def __init__(self, socket):
        self.socket = socket
        self.uid = None
        self.__route = {
                "new": self.newUser, 
                "online": self.updateSocket,
                "newroom": self.newRoom,
                "join": self.joinRoom,
                "chat": self.chat
                }

    def Ctrl(self, reqBinary):
        data = json.loads(reqBinary.decode())
        method = data["method"]
        if self.uid is None:
            self.uid = data.get("uid")
        res = self.__route[method](data)
        res["method"] = method
        res["status"] = "ok"
        return res

    def newUser(self, data):
        ## uid: user id
        ## sid: security id
        self.uid = users.createUser(self.socket)
        self.sid = int(time.time())
        mctrl.signUp(self.uid, self.sid)
        return {"uid": self.uid, "sid": hex(self.sid)[2:]}

    def updateSocket(self, data):
        self.uid = data["uid"]
        users.updateSocket(self.uid, self.socket)
        return {"uid": self.uid}

    def stopSocket(self):
        users.removeSocket(self.uid)

    def newRoom(self, data):
        roomid, createtime = mctrl.newRoom(**data)
        return {"roomid": roomid, "createtime": createtime}

    def joinRoom(self, data):
        res = mctrl.joinRoom(data["roomid"], self.uid)
        return res

    def chat(self, data):
        members, time = mctrl.chatRoom(**data)
        data["time"] = time
        data["status"] = "ok"
        for member in members:
            if member!=self.uid:
                users.sendSocket(member, data)
        return {"uid": self.uid, "time": time}

