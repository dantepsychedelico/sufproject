
## python mongo model

import pymongo, time

CONFIG = {
        "DB_HOST": "127.0.0.1", 
        "DB_PORT": 27017,
        "DB_NAME": "test"
        }

class mongoModel:
    def __init__(self, DB_HOST, DB_PORT, DB_NAME):
        self.client = pymongo.MongoClient(DB_HOST, DB_PORT)
        self.db = self.client[DB_NAME]

    def createUser(self, uid, sid):
        self.db.users.insert({"uid": uid, "sid": sid, 
            "createtime": int(time.time())})
    
    def createRoom(self, roomid, uid, roomname, alivetime):
        createtime = int(time.time())
        self.db.rooms.insert({"roomid": roomid, "createid": uid, 
            "members": [uid], "createtime": createtime,
            "alivetime": alivetime, "roomname": roomname})

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

mongo = mongoModel(**CONFIG)
