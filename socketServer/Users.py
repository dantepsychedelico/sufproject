from struct import pack
from mongoCtrl import mongoCtrl as mCtrl
from socketProtocal import socketProtocal as protocal
import logging, json

class Users:
    currentUid = mCtrl.getMaxUid()
    onlineSockets = {}

    def createUser(self, socketConnect):
        self.currentUid += 1
        self.onlineSockets[self.currentUid] = socketConnect
        return self.currentUid

    def updateSocket(self, uid, socketConnect):
        self.onlineSockets[uid] = socketConnect

    def removeSocket(self, uid):
        if uid in self.onlineSockets:
            self.onlineSockets.pop(uid)

    def sendSocket(self, uid, res):
        buflen, resBinary = protocal.encrypt(json.dumps(res).encode())
        print(pack('!H', buflen)+resBinary)
        socket = self.onlineSockets[uid]
        socket.sendall(pack('!H', buflen)+resBinary)
        logging.info("{} report: length {}".format(socket.getpeername(), buflen))

users = Users()
