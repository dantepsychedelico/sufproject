#!/usr/bin/env python3
#
# the e2e testing
import socket, struct, json

HOST = 'localhost'
PORT = 30000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

data = {"method": "new"}
bson = json.dumps(data).encode()
res = struct.pack('!H', len(bson))+bson
print("start connect")
print(res)
s.sendall(res)
getdata = s.recv(1024)
print('Received', repr(getdata))
jj = json.loads(getdata[2:].decode())

data = {"method": "online", "uid": jj["uid"]}
bson = json.dumps(data).encode()
res = struct.pack('!H', len(bson))+bson
print(res)
s.sendall(res)
getdata = s.recv(1024)
print('Received', repr(getdata))

s.close()
