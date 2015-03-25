
import json, time

from Users import Users
from mongoCtrl import mongoCtrl as mCtrl

class router:
    mctrl = mCtrl()

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
        self.mctrl.signUp(self.uid, self.sid)
        return {"uid": self.uid, "sid": hex(self.sid)[2:]}

    def updateSocket(self, data):
        Users.updateSocket(self.socket)
        return {"uid": self.uid}

    def stopSocket(self):
        Users.removeSocket(self.uid)

    def newRoom(self, data):
        return

    def joinRoom(self, data):
        return 

    def resolve(self, reqjson):
        method = reqjson["method"]
        if method == "new":
            user = User()
            user.setSocket(self)
            users[user.id] = user
            rjson = {"status": "ok", "id": user.id}
        elif method == "online":
            user = User(reqjson["id"])
            user.setSocket(self)
            users[user.id] = user
            rjson = {"status": "ok"}
        elif method == "newroom":
            room = Room()
            room.addMember(reqjson["id"])
            rooms[room.roomId] = room   ## save room status
            rjson = { "status": "ok", "roomid": room.roomId, 
                    "roomname": reqjson["roomname"],
                    "members": room.getMembers(),
                    "createtime": int(time.time()),
                    "alivetime": reqjson["alivetime"]}
            print(room.members)
        elif method == "join":
            room = rooms[reqjson["roomid"]]
            room.addMember(reqjson["id"])
            rjson = {"status": "ok", "roomid": room.roomId,
                    "members": room.getMembers(), "alivetime": 1000,
                    "createtime": 1426858964, "roomname": "room"}
            print(room.members)
        elif method == "chat":
            uid = reqjson["id"]
            room = rooms[reqjson["roomid"]]
            fjson = {"status": "ok", "id": uid, "roomid": reqjson["roomid"], 
                    "type": reqjson["type"], "content": reqjson["content"], 
                    "time": int(time.time())}
            for memberId in room.members:
                if memberId==uid:
                    continue
                else:
                    fjson["method"] = "chat"
                    bjson = json.dumps(fjson).encode()
                    users[memberId].socket.request.sendall(struct.pack('!H', len(bjson))+bjson)
            rjson = {"stauts": "ok", "id": uid}
        else:
            assert False, "unknown method: {}".format(method)
        rjson["method"] = method
        return rjson
