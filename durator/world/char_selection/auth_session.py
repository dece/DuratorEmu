from struct import Struct


class AuthSessionHandler(object):

    def __init__(self, connection, packet):
        self.conn = connection
        self.packet = packet

    def process(self):
        self._parse_packet(self.packet)
        return None, b""

    def _parse_packet(self, packet):
        pass
