#!/usr/bin/env python3
#
# the e2e testing
import socket, struct, json

HOST = 'localhost'    # The remote host
PORT = 30000              # The same port as used by the server
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

data = {"method": "online", "id": 1}
bson = json.dumps(data).encode()
res = struct.pack('!H', len(bson))+bson
print(res)
s.sendall(res)
getdata = s.recv(1024)
print('Received', repr(getdata))

s.close()
