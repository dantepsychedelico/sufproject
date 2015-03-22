
from mongoCtrl import mongoCtrl as mCtrl

DB_HOST = "127.0.0.1"
DB_PORT = 27017
DB_NAME = "test"

class Users:
    currentUid = mCtrl(DB_HOST, DB_PORT, DB_NAME).getMaxUid()
    onlineSockets = {}

    @classmethod
    def createUser(cls, socketConnect):
        cls.currentUid += 1
        cls.onlineSockets[cls.currentUid] = socketConnect
        return cls.currentUid

    @classmethod
    def updateSocket(cls, socketConnect):
        cls.onlineSockets[cls.currentUid] = socketConnect

    @classmethod
    def removeSocket(cls, uid):
        cls.onlineSockets.pop(uid)
