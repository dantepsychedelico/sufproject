import os
os.sys.path.append(os.path.dirname(os.getcwd()))
import socket, json, struct
from socketProtocal import socketProtocal as protocal

class socketTest:
    def __init__(self, HOST, PORT):
        self.HOST = HOST
        self.PORT = PORT

    def producer(self, reqjson):
        buflen, reqBinary = protocal.encrypt(json.dumps(reqjson).encode())
        req = struct.pack('!H', buflen)+reqBinary
        self.client.sendall(req)
        return self

    def comsumer(self):
        header = self.client.recv(2)
        buflen, = struct.unpack('!H', header)
        res = self.client.recv(2**(buflen-1).bit_length())
        return json.loads(protocal.decrypt(res).decode())

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.HOST, self.PORT))
        return self

    def disconnect(self):
        self.client.close()
        return self

if __name__  == "__main__":
    HOST = "127.0.0.1"
    PORT = 30000
    st = socketTest(HOST, PORT)
    st.connect()
    print(st.producer({"method": "new"}).comsumer())
    st.disconnect()
