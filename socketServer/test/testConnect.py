#!/bin/python3
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
s.close()
print('Received', repr(getdata))
