from struct import Struct
import time

from pyshgck.logger import LOG


class RealmConnection(object):

    def __init__(self, server, connection, address):
        self.server = server
        self.socket = connection
        self.address = address

    def handle_connection(self):
        data = self._get_whole_packet()
        if data is None:
            return
        realm_state = RealmConnection._parse_realm_packet(data)
        self._handle_realm_state(realm_state)
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

    @staticmethod
    def _parse_realm_packet(packet):
        """ Parse that realm packet and return the realm state it describes. """
        realm_state = {}
        offset = 1

        name_size = packet[offset]
        offset += 1

        realm_state["name"] = packet[offset : offset+name_size]
        realm_state["name"] = realm_state["name"].decode("ascii")
        offset += name_size

        float_struct = Struct("f")
        float_bytes = packet[offset : offset+float_struct.size]
        realm_state["population"] = float_struct.unpack(float_bytes)[0]
        offset += float_struct.size

        address_size = packet[offset]
        offset += 1

        realm_state["address"] = packet[offset : offset+address_size]
        realm_state["address"] = realm_state["address"].decode("ascii")
        offset += address_size

        return realm_state

    def _handle_realm_state(self, realm_state):
        realm_name = realm_state["name"]
        LOG.debug("Updating informations about realm " + realm_name)
        realm_state["last_update"] = time.time()

        with self.server.locks["realms"]:
            self.server.realms[realm_name] = realm_state
        self.server.maintain_realm_list()
