import math
from struct import Struct

from pyshgck.bin import read_struct


class Position(object):

    BIN = Struct("<4f")

    def __init__(self, x = 0.0, y = 0.0, z = 0.0, o = 0.0):
        self.x = x
        self.y = y
        self.z = z
        self.o = o

    @staticmethod
    def from_io(bytes_io):
        position = Position()
        position_data = read_struct(bytes_io, Position.BIN)
        position.x = position_data[0]
        position.y = position_data[1]
        position.z = position_data[2]
        position.o = position_data[3]
        return position

    def to_bytes(self):
        return self.BIN.pack(self.x, self.y, self.z, self.o)

    def distance_from(self, other_pos):
        return math.sqrt( (self.x - other_pos.x)**2 +
                          (self.y - other_pos.y)**2 +
                          (self.z - other_pos.z)**2 )
