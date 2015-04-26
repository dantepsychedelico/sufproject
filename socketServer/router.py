
import json, time

from Users import users
from mongoCtrl import mongoCtrl as mctrl

class router:
    def __init__(self, socket):
        """ every online user have one router object and used 'Ctrl' method to control request and response """
        self.socket = socket
        self.uid = None
        self.token = None
        self.__route = {
                "new": self.newUser, 
                "online": self.updateSocket,
                "newroom": self.newRoom,
                "join": self.joinRoom,
                "chat": self.chat,
                "updateToken": self.updateToken
                }

    def Ctrl(self, reqBinary):
        data = json.loads(reqBinary.decode())
        method = data["method"]
        if self.uid is None:
            self.uid = data.get("uid")
        res = self.__route[method](data)
        res["method"] = method
        if "status" not in res:
            res["status"] = "ok"
        return res

    def newUser(self, data):
        """ uid: userid; sid: security id """
        self.uid = users.createUser(self.socket)
        self.sid = int(time.time())
        mctrl.signUp(self.uid, self.sid)
        return {"uid": self.uid, "sid": hex(self.sid)[2:]}

    def updateSocket(self, data):
        """ update socket connection for the same user """
        self.uid = data["uid"]
        users.updateSocket(self.uid, self.socket)
        return {"uid": self.uid}

    def updateToken(self, data):
        """ update token for IOS device"""
        self.token = data["token"]
        self.uid = data["uid"]
        self.sid = data["sid"]
        mctrl.receiveToken(self.uid, self.sid, self.token)
        return {"token": self.token}

    def stopSocket(self):
        """ remove the socket connection for the user """
        users.removeSocket(self.uid)

    def newRoom(self, data):
        """ """
        roomid, createtime = mctrl.newRoom(**data)
        return {"roomid": roomid, "createtime": createtime}

    def joinRoom(self, data):
        res = mctrl.joinRoom(data["roomid"], self.uid)
        return res

    def chat(self, data):
        members, time = mctrl.chatRoom(**data)
        data["time"] = time
        data["status"] = "getok"
        for member in members:
            if member!=self.uid:
                users.sendSocket(member, data)
        return {"uid": self.uid, "time": time, "status": "sendok"}

