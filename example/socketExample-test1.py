#!/usr/bin/env python3
#
# the e2e testing
import socket, struct, json, sys

HOST = sys.argv[1]
PORT = int(sys.argv[2])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

data = {"method": "new"}
bson = json.dumps(data).encode()
res = struct.pack('!H', len(bson))+bson
print("start connect")
print(res)
s.sendall(res)
s.close()
