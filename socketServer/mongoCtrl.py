
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
        createtime = mongo.createRoom(__class__.currentRoomId, uid, roomname, alivetime)
        return __class__.currentRoomId, createtime

mctrl = mongoCtrl()
