#!/usr/bin/python3

import socketserver, json, struct
from router import router
from socketProtocal import socketProtocal as protocal

## debug and log tools
import sys, logging, traceback
LOG_FILE = "python-socket-server.log"
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, \
            format='%(asctime)s %(message)s')
##

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
            clientIp = self.client_address[0]
            rt = router(self.request)
            while True:
                header = self.request.recv(2)
                if not bool(header):
                    logging.info("stop conn: {}".format(self.client_address[0]))
                    return
                buflen, = struct.unpack('!H', header)
                logging.info("{} wrote: length {}".format(clientIp, buflen))
                reqBinary = protocal.decrypt(self.request.recv(buflen))
                print(struct.pack('!H', buflen)+reqBinary)
                buflen, resBinary = protocal.encrypt(rt.Ctrl(reqBinary))
                print(struct.pack('!H', buflen)+resBinary)
                self.request.sendall(struct.pack('!H', buflen)+resBinary)
                logging.info("{} report: length {}".format(clientIp, buflen))
        except BaseException:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            with open(LOG_FILE, "a") as fn:
                traceback.print_exception(exc_type, exc_value, exc_traceback, file=fn)
            print (traceback.print_exc())
            self.request.close()
            rt.stopSocket()
            return

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

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
    HOST = argv[1] if len(argv) > 1 else "127.0.0.1"
    PORT = argv[2] if len(argv) > 2 else 30000

    # used $python3 pySocketServer.py localhost 9999
    # Create the server, binding to localhost on port argv[1]
    server = ThreadedTCPServer((HOST, PORT), MyTCPHandler)
    socketserver.TCPServer.allow_reuse_address = True

    ## chat {"method": "chat", "id": 1, "roomid": 10, type: "content", "content": "hello"}
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

