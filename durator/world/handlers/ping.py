from struct import Struct

from durator.world.opcodes import OpCode
from durator.world.world_packet import WorldPacket


class PingHandler(object):

    PACKET_BIN = Struct("<I")

    def __init__(self, connection, packet):
        self.conn = connection
        self.packet = packet
        self.ping_value = 0

    def process(self):
        pong_packet = WorldPacket(self.packet)
        pong_packet.opcode = OpCode.SMSG_PONG
        return None, pong_packet
