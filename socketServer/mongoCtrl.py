
from mongoModel import mongo

class mongoCtrl:
    currentRoomId = mongo.getMaxRoomId()

    @staticmethod
    def signUp(uid, sid):
        mongo.createUser(uid, sid)

    @staticmethod
    def getMaxUid():
        return mongo.getMaxUid()

    @staticmethod
    def getMaxRoomId():
        return mongo.getMaxRoomid()

    @staticmethod
    def newRoom(uid, roomname, alivetime):
        __class__.currentRoomId += 1
        createtime = mongo.updateRoom(__class__.currentRoomId, uid, 
                roomname, alivetime)
        return __class__.currentRoomId, createtime

    @staticmethod
    def joinRoom(roomid, uid):
        room = mongo.readRoom(roomid, ["roomid", "members", "roomname", 
            "creattime", "alivetime"])
        members = room["members"]
        if uid not in members:
            members.append(uid)
            mongo.updateRoom(roomid, members = members)
        return room

    @staticmethod
    def chatRoom(roomid, msg):
        members = mongo.readRoom(roomid, ["members"])["members"]
        msg = mongo.pushRoomMsg(roomid, msg)
        return members, msg

mctrl = mongoCtrl()
