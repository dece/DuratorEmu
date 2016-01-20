import time
from struct import Struct

from durator.world.opcodes import OpCode
from durator.world.world_packet import WorldPacket


class QueryTimeHandler(object):
    """ Send name associated to a GUID to the client. """

    RESPONSE_BIN = Struct("<I")

    def __init__(self, connection, packet):
        self.conn = connection
        self.packet = packet

        self.guid = -1

    def process(self):
        seconds = int(time.time())
        response_data = self.RESPONSE_BIN.pack(seconds)
        response = WorldPacket(OpCode.SMSG_QUERY_TIME_RESPONSE, response_data)
        return None, response
