#!/usr/bin/python3
import socketserver, json

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
        while True:
            # self.request is the TCP socket connected to the client
            self.data = self.request.recv(1024).strip()
            print("{} wrote:".format(self.client_address[0]))
            print(self.data)
            # just send back the same data, but upper-cased
            if bool(self.data):
                rjson = self.resolve(json.loads(self.data.decode().strip('\x00\x06')))
                self.request.sendall(b'\x00\x06'+json.dumps(rjson).encode())
            else:
                print("stop conn: {}".format(self.client_address[0]))
                return

    def resolve(self, sjson):
        method = sjson["method"]
        if method == "new":
            user = User()
            user.setSocket(self)
            users[user.id] = user
            rjson = {"status": "ok", "id": user.id}
        elif method == "online":
            user = User(sjson["id"])
            user.setSocket(self)
            users[user.id] = user
            rjson = {"status": "ok"}
        elif method == "newroom":
            room = Room()
            room.addMember(sjson["id"])
            rooms[room.id] = room
            rjson = {"status": "ok", "room": room.id}
            print(room.members)
        elif method == "join":
            room = rooms[sjson["room"]]
            room.addMember(sjson["id"])
            rjson = {"status": "ok", "room": room.id}
            print(room.members)
        elif method == "chat":
            uid = sjson["id"]
            room = rooms[sjson["room"]]
            fjson = {"status": "chat", "id": uid, "room": sjson["room"], 
                    "text": sjson["text"]}
            for ruid in room.members:
                if ruid==uid:
                    continue
                else:
                    users[ruid].socket.request.sendall(b'\x00\x06'+json.dumps(fjson).encode())
            rjson = {"stauts": "ok"}
        else:
            assert False, "unknown method: {}".format(method)
        return rjson

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
    id = 0
    def __init__(self, rid=0):
        self.members = set()
        if rid:
            self = rooms[rid]
        else:
            self.__class__.id += 1

    def addMember(self, uid):
        self.members.add(uid)

if __name__ == "__main__":
    from sys import argv
    HOST, PORT = argv[1], int(argv[2])

    # used $python3 pySocketServer.py localhost 9999
    # Create the server, binding to localhost on port argv[1]
    server = ThreadedTCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
