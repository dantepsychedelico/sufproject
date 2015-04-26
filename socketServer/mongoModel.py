
## python mongo model

import pymongo, time
from os import getenv

DB_HOST= getenv("DB_PORT_27017_TCP_ADDR", "127.0.0.1")
DB_PORT= int(getenv("DB_PORT_27017_TCP_PORT", 27017))
DB_NAME= getenv("DB_COLLECTION", "test")

class mongoModel:
    def __init__(self, DB_HOST, DB_PORT, DB_NAME):
        self.client = pymongo.MongoClient(DB_HOST, DB_PORT)
        self.db = self.client[DB_NAME]

    def createUser(self, uid, sid):
        self.db.users.insert({"uid": uid, "sid": sid, 
            "createtime": int(time.time()), "token": None})

    def updateUser(self, uid, sid, **args):
        self.db.users.update({
            "uid": uid,
            "sid": sid
            }, {"$set": args,
                "$currentDate": {"last": True }
                })

    def writeToken(self,uid ,sid , token):
        self.db.users.update({
            "uid": uid,
            "sid": sid,
            "token": token
            })

    def readToken(self, uid):
        cur = self.db.users.find({"uid": uid})
        if cur.count():
            return cur[0]["token"]
        else:
            return None

    def createRoom(self, roomid, uid, roomname, alivetime):
        createtime = int(time.time())
        self.db.rooms.insert({"roomid": roomid, 
            "createid": uid, 
            "members": [uid], 
            "createtime": createtime,
            "alivetime": alivetime, 
            "roomname": roomname,
            "msg": []})
        return createtime

    def readRoom(self, roomid, keys):
        cur = self.db.rooms.find({"roomid": roomid},
                {key: 1 for key in keys})
        assert cur.count() == 1, "readRoom non unique"
        room = cur[0]
        room.pop("_id")
        return room



    def updateRoom(self, roomid, **args):
        self.db.rooms.update({
            "roomid": roomid 
            }, {"$set": args,
                "$currentDate": {"last": True }
                })
    ## mtype: msg type; mtext: msg text
    def pushRoomMsg(self, roomid, uid, mtype, content, **args):
        msg = {"uid": uid, "mtype": mtype, "content": content,
                "time": int(time.time())}
        self.db.rooms.update({
            "roomid": roomid
            }, {"$push": {"msg": {"$each": [msg]}},
                "$currentDate": {"last": True}
                })
        return msg

    def getMaxUid(self):
        cur = self.db.users.find().sort("uid", pymongo.DESCENDING).limit(1)
        if cur.count():
            return int(cur[0]["uid"])
        else:
            return 0

    def getMaxRoomId(self):
        cur = self.db.rooms.find().sort("roomid", pymongo.DESCENDING).limit(1)
        if cur.count():
            return int(cur[0]["roomid"])
        else:
            return 0

mongo = mongoModel(DB_HOST, DB_PORT, DB_NAME)
