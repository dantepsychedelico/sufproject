
class Users:
    currentUid = 0
    onlineSockets = {}

    @classmethod
    def createUser(cls, socketConnect):
        cls.currentUid += 1
        onlineSockets[cls.currentUid] = socketConnect
        return cls.currentUid

    @classmethod
    def modifySocket(cls, socketConnect):
        onlineSockets[cls.currentUid] = socketConnect
