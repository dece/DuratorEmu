from struct import Struct

from durator.world.opcodes import OpCode
from durator.world.world_packet import WorldPacket


class RequestAccountDataHandler(object):

    REQUEST_BIN = Struct("<I")

    # # uint32 type
    # # uint32 unk
    # # And then a big buffer
    # HEADER_BIN = Struct("<2I")

    def __init__(self, connection, packet):
        self.conn = connection
        self.packet = packet

        self.requested_flags = 0

    def process(self):
        self._parse_packet(self.packet)
        # response_data = self.HEADER_BIN.pack(0, 0)
        # return None, WorldPacket(OpCode.SMSG_UPDATE_ACCOUNT_DATA, response_data)
        return None, None

    def _parse_packet(self, packet):
        self.flags = self.REQUEST_BIN.unpack(packet)
