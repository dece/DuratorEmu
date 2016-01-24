from struct import Struct


class ZoneUpdateHandler(object):
    """ Handle all player movement opcodes. """

    PACKET_BIN = Struct("<I")

    def __init__(self, connection, packet):
        self.conn = connection
        self.packet = packet

        self.zone_id = 0

    def process(self):
        self._parse_packet(self.packet)
        self.conn.player.zone_id = self.zone_id
        return None, None

    def _parse_packet(self, packet):
        self.zone_id = self.PACKET_BIN.unpack(packet)[0]
