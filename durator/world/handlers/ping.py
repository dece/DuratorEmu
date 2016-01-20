from struct import Struct

from durator.world.opcodes import OpCode
from durator.world.world_packet import WorldPacket


class PingHandler(object):
    """ Answer to a ping from client. """

    PACKET_BIN = Struct("<I")

    def __init__(self, connection, packet):
        self.conn = connection
        self.packet = packet

    def process(self):
        pong_packet = WorldPacket(OpCode.SMSG_PONG, self.packet)
        return None, pong_packet
