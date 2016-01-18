from struct import Struct


class Position(object):

    BIN = Struct("<4I")

    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.o = 0.0

    def to_bytes(self):
        return self.BIN.pack(self.x, self.y, self.z, self.o)
