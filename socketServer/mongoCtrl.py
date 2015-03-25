
from mongoModel import mongo

class mongoCtrl:
    mongo = mongo

    def signUp(self, uid, sid):
        self.mongo.createUser(uid, sid)

    @classmethod
    def getMaxUid(cls):
        return cls.mongo.getMaxUid()

