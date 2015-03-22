#!/usr/bin/python3
import socketserver, json, struct

from router import router

from socketProtocal import socketProtocal as protocal

## debug and log tools
import sys, logging, traceback
LOG_FILE = "python-socket-server.log"
logging.basicConfig(filename='example.log', level=logging.DEBUG, \
            format='%(asctime)s %(message)s')


users = {}
rooms = {}
class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def handle(self):
        logging.info("start conn {}".format(self.client_address[0]))
        try:
            while True:
                header = self.request.recv(2)
                if not bool(header):
                    logging.info("stop conn: {}".format(self.client_address[0]))
                    return
                # self.request is the TCP socket connected to the client
                buflen, = struct.unpack('!H', header)
                clientIp = self.client_address[0]
                logging.info("{} wrote: length {}".format(clientIp, buflen))
                response = protocal.decrypt(self.request.recv(buflen))
                protocal.encrypt
                logging.info("{} report: length {}".format(clientip, md.reportBuflen))
        except BaseException:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback, file=LOG_FILE)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class User:
    id = 0
    def __init__(self, uid=0):
        if uid:
            self.id = uid
        else:
            self.__class__.id += 1

    def setSocket(self, conn):
        self.socket = conn

class Room:
    maxRoomId = 0
    def __init__(self, roomId=0):
        self.members = set()
        if roomId:
            self = rooms[roomId]
        else:
            self.__class__.maxRoomId += 1
            self.roomId = self.maxRoomId

    def addMember(self, uid):
        self.members.add(uid)

    def getMembers(self):
        return list(self.members)

if __name__ == "__main__":
    from sys import argv
    HOST, PORT = argv[1], int(argv[2])

    # used $python3 pySocketServer.py localhost 9999
    # Create the server, binding to localhost on port argv[1]
    server = ThreadedTCPServer((HOST, PORT), MyTCPHandler)

    ## chat {"method": "chat", "id": 1, "roomid": 10, type: "content", "content": "hello"}
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

