#!/usr/bin/python3

import socketserver, json, struct
from router import router
from socketProtocal import socketProtocal as protocal
from Users import users

## debug and log tools
import sys, logging, traceback
##

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def handle(self):
        logging.info("start conn {}".format(self.client_address[0]))
        print("start conn {}".format(self.client_address[0]))
        try:
            clientIp = self.client_address[0]
            rt = router(self.request)
            while True:
                header = self.request.recv(2)
                if not bool(header):
                    logging.info("stop conn: {}".format(self.client_address[0]))
                    return
                buflen, = struct.unpack('!H', header)
                logging.info("{} wrote: length {}".format(clientIp, buflen))
                reqBinary = protocal.decrypt(self.request.recv(2**(buflen-1).bit_length()))
                print(struct.pack('!H', buflen)+reqBinary)
                res = rt.Ctrl(reqBinary)
                users.sendSocket(rt.uid, res)
        except BaseException:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            with open(LOG_FILE, "a") as fn:
                traceback.print_exception(exc_type, exc_value, exc_traceback, file=fn)
            print (traceback.print_exc())
            self.request.close()
            rt.stopSocket()
            return

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """ this class is enable socket thread"""
    pass

if __name__ == "__main__":
    from sys import argv
    from os import getenv
    HOST = argv[1] if len(argv) > 1 else getenv("HOST", "127.0.0.1")
    PORT = int(argv[2]) if len(argv) > 2 else int(getenv("PORT", 3000))
    LOG_FILE = getenv("LOG_FILE", "log/python-socket-server.log")
    logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, \
                format='%(asctime)s %(message)s')

    server = ThreadedTCPServer((HOST, PORT), MyTCPHandler)
    socketserver.TCPServer.allow_reuse_address = True

    # interrupt the program with Ctrl-C
    server.serve_forever()

