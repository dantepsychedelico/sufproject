#!/usr/bin/env python3
#
# the e2e testing
# testing twice socket: 1-header, 2-data
import socket, struct, json

HOST = 'localhost'
PORT = 30000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

data = {"method": "testing"}
bson = json.dumps(data).encode()
print("start connect")
print(struct.pack('!H', len(bson)))
s.sendall(struct.pack('!H', len(bson)))
print(bson)
s.sendall(bson)
getdata = s.recv(1024)
print('Received', repr(getdata))

s.close()

