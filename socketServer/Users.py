from mongoCtrl import mongoCtrl as mCtrl

class Users:
    currentUid = mCtrl.getMaxUid()
    onlineSockets = {}

    @classmethod
    def createUser(cls, socketConnect):
        cls.currentUid += 1
        cls.onlineSockets[cls.currentUid] = socketConnect
        return cls.currentUid

    @classmethod
    def updateSocket(cls, uid, socketConnect):
        cls.onlineSockets[uid] = socketConnect

    @classmethod
    def removeSocket(cls, uid):
        cls.onlineSockets.pop(uid)
