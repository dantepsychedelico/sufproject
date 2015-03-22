
from mongoModel import mongoModel

class mongoCtrl:
    def __init__(self, DB_HOST, DB_PORT, DB_NAME):
        self.model = mongoModel(DB_HOST, DB_PORT, DB_NAME)

    def signUp(self, uid, sid):
        self.model.createUser(uid, sid)

    def getMaxUid(self):
        return self.model.getMaxUid()
