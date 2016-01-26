import io
import time

from pyshgck.bin import read_cstring


class RealmConnection(object):
    """ Handle the connection with a world server to update the local login
    server realm state list. """

    def __init__(self, server, connection, address):
        self.server = server
        self.socket = connection
        self.address = address

        self.realm_name = ""

    def handle_connection(self):
        data = self._get_whole_packet()
        if data is None:
            return

        realm_info_packet = data[1:]
        self._parse_realm_info_packet(realm_info_packet)
        realm_state = self._get_realm_state(realm_info_packet)
        self._register_realm_state(realm_state)

        self.socket.close()

    def _get_whole_packet(self):
        data = self.socket.recv(1024)
        if not data:
            return None

        packet_size = data[0]
        while len(data[1:]) < packet_size:
            data_part = self.socket.recv(1024)
            if not data_part:
                return None
            data += data_part

        return data

    def _parse_realm_info_packet(self, packet):
        """ Parse that realm packet and grab the realm name. """
        packet_io = io.BytesIO(packet)
        self.realm_name = read_cstring(packet_io, 5).decode("ascii")

    def _get_realm_state(self, packet):
        realm_state = { "packet": packet, "last_update": time.time() }
        return realm_state

    def _register_realm_state(self, realm_state):
        with self.server.locks["realms"]:
            self.server.realms[self.realm_name] = realm_state
