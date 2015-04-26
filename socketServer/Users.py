from struct import pack
from mongoCtrl import mongoCtrl as mCtrl
from socketProtocal import socketProtocal as protocal
from sendRemoteNotify import sendRemoteNotify as remoteNotify
import logging, json

class Users:
    currentUid = mCtrl.getMaxUid()
    onlineSockets = {}

    def createUser(self, socketConnect):
        self.currentUid += 1
        self.onlineSockets[self.currentUid] = socketConnect
        return self.currentUid

    def updateSocket(self, uid, socketConnect):
        if uid in self.onlineSockets:
            if self.onlineSockets[uid] is not socketConnect:
                self.onlineSockets[uid].close()
        self.onlineSockets[uid] = socketConnect


    def removeSocket(self, uid):
        if uid in self.onlineSockets:
            self.onlineSockets.pop(uid)

    def sendSocket(self, uid, res):
        buflen, resBinary = protocal.encrypt(json.dumps(res).encode())
        if self.onlineSockets[uid] != None:
            socket = self.onlineSockets[uid]
            logging.info("{} report: length {}".format(socket.getpeername(), buflen))
            logging.debug(pack('!H', buflen)+resBinary)
            socket.sendall(pack('!H', buflen)+resBinary)
        elif mCtrl.getToken(uid) != None:
            remoteNotify.sendNotify()


users = Users()
