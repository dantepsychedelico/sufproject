#!/usr/bin/python3
import ssl, socket, json, struct
1234
class sendRemoteNotify:
    token = "052d6cef 405314c7 6b186dd4 848af9ee 2c721bd9 33562fbd 2e7535e5 f4ca298e"

    thePayLoad = {
        "aps": {
             "alert":"Oh no! Server's Down!",
             "sound":"k1DiveAlarm.caf",
             "badge":42,
            },
        "test_data": { "foo": "bar" },
    }

    apnHost = ( "gateway.sandbox.push.apple.com", 2195 )

    def sendNotify(self):
        data = json.dumps( thePayLoad )
        # Clear out spaces in the device token and convert to hex
        byteToken = bytes.fromhex( token.replace(" ","") ) # Python 3
        theFormat = '!BH32sH%ds' % len(data)
        theNotification = struct.pack( theFormat, 0, 32, byteToken, len(data), str.encode(data))
        # Create our connection using the certfile saved locally
        # ssl_sock = ssl.wrap_socket( socket.socket( socket.AF_INET, socket.SOCK_STREAM ), certfile="PushChatCert.pem", keyfile="PushChatKey.pem" )
        ## or
        ssl_sock = ssl.wrap_socket( socket.socket( socket.AF_INET, socket.SOCK_STREAM ), certfile="ck.pem")
        ssl_sock.connect( apnHost )
        ssl_sock.write( theNotification )
        ssl_sock.close()

sendremote = sendRemoteNotify()