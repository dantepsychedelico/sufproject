#!/usr/bin/python3
import socketserver, json, struct

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
            print("start conn {}".format(self.client_address[0]))
            data = self.request.recv(2)
            if bool(data):
                buflen, = struct.unpack('!H', data)
                data = self.request.recv(buflen)
                clientip = self.client_address[0]
                print("{} wrote: {}".format(clientip, data))
                rjson = self.resolve(json.loads(data.decode()))
                bjson = json.dumps(rjson).encode()
                print("{} report: {}".format(clientip, struct.pack('!H', len(bjson))+bjson))
                self.request.sendall(struct.pack('!H', len(bjson))+bjson)
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
                    fjson["method"] = "chat"
                    bjson = json.dumps(fjson).encode()
                    users[ruid].socket.request.sendall(struct.pack('!H', len(bjson))+bjson)
            rjson = {"stauts": "ok", "id": uid}
        else:
            assert False, "unknown method: {}".format(method)
        rjson["method"] = method
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
