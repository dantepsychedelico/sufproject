import struct

class socketProtocal:

    @staticmethod
    def encrypt(stream, method="ssl"):
        return len(stream), stream

    @staticmethod
    def decrypt(stream, method="ssl"):
        return stream
