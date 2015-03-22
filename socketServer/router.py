
import json, time

class router:

    def __init__(self, buflen, request):
        self.buflen = buflen
        self.request = request

    def Ctrl(self):
        self.data = json.loads(self.request.recv(self.buflen).decode())
        bjson = json.dumps(self.resolve(json.loads(data.decode()))).encode()
        self.request.sendall(struct.pack('!H', len(bjson))+bjson)
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
