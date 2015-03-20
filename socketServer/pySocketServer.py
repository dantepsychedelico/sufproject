#!/usr/bin/python3
import socketserver, json, struct, time

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

    def resolve(self, reqjson):
        method = reqjson["method"]
        if method == "new":
            user = User()
            user.setSocket(self)
            users[user.id] = user
            rjson = {"status": "ok", "id": user.id}
        elif method == "online":
            user = User(reqjson["id"])
            user.setSocket(self)
            users[user.id] = user
            rjson = {"status": "ok"}
        elif method == "newroom":
            room = Room()
            room.addMember(reqjson["id"])
            rooms[room.roomId] = room   ## save room status
            rjson = { "status": "ok", "roomid": room.roomId, 
                    "roomname": reqjson["roomname"],
                    "members": room.getMembers(),
                    "createtime": int(time.time()),
                    "alivetime": reqjson["alivetime"]}
            print(room.members)
        elif method == "join":
            room = rooms[reqjson["roomid"]]
            room.addMember(reqjson["id"])
            rjson = {"status": "ok", "roomid": room.roomId,
                    "members": room.getMembers(), "alivetime": 1000,
                    "createtime": 1426858964, "roomname": "room"}
            print(room.members)
        elif method == "chat":
            uid = reqjson["id"]
            room = rooms[reqjson["roomid"]]
            fjson = {"status": "ok", "id": uid, "roomid": reqjson["roomid"], 
                    "type": reqjson["type"], "content": reqjson["content"], 
                    "time": int(time.time())}
            for memberId in room.members:
                if memberId==uid:
                    continue
                else:
                    fjson["method"] = "chat"
                    bjson = json.dumps(fjson).encode()
                    users[memberId].socket.request.sendall(struct.pack('!H', len(bjson))+bjson)
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
