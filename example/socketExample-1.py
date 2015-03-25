#!/usr/bin/env python3
import socketserver, time

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
#        time.sleep(1)
        while True:
            self.data = self.request.recvmsg(1024)
            print ("{} wrote: ".format(self.client_address[0]), self.data)
            if not bool(self.data[0]):
                print("stop conn")
                return
            # just send back the same data, but upper-cased
#            self.request.sendall(self.data)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
if __name__ == "__main__":
    from sys import argv
    HOST, PORT = argv[1], int(argv[2])

    socketserver.TCPServer.allow_reuse_address = True
    server = ThreadedTCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
