from durator.auth.constants import LoginOpCodes


class RealmlistRequest(object):

    HEADER_SIZE = 7

    def __init__(self, connection, packet):
        self.conn = connection
        self.packet = packet

    def process(self):
        realm_list = self.conn.server.get_realm_list()
        realm_list = {}
        realm_infos = self._get_realm_info_packets(realm_list)
        response = self._add_realm_infos_header(realm_infos, len(realm_list))
        return None, response

    def _get_realm_info_packets(self, realm_list):
        packets = [None] * len(realm_list)
        for index, realm_name in enumerate(realm_list):
            realm = realm_list[realm_name]
            realm_info = self._get_realm_info_packet(realm)
            packets[index] = realm_info
        return b"".join(packets)

    def _get_realm_info_packet(self, realm):
        packet = b""
        packet += b"\x00"  # icon ?
        packet += b"\x00"  # flags ?
        packet += realm["name"].encode("ascii") + b"\x00"
        packet += realm["address"].encode("ascii") + b"\x00"
        packet += b"\x00"  # num_chars ?
        packet += b"\x00"  # timezone ?
        # packet += b"\x00"  # unknown ?
        return packet

    def _add_realm_infos_header(self, realm_infos, num_realms):
        header = b""
        header += int.to_bytes(LoginOpCodes.REALMLIST.value, 1, "little")
        full_packet_size = RealmlistRequest.HEADER_SIZE + len(realm_infos)
        header += int.to_bytes(full_packet_size, 2, "little")
        header += int.to_bytes(0, 4, "little")  # unknown
        header += int.to_bytes(num_realms, 1, "little")
        return header + realm_infos
