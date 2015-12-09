from struct import Struct

from durator.auth.constants import LoginOpCodes


class RealmlistRequest(object):

    MIN_RESPONSE_SIZE = 7

    RESPONSE_HEADER_BIN = Struct("<BHIB")
    RESPONSE_FOOTER_BIN = Struct("<H")
    REALM_PACKET_FMT = "<IB{name_len}s{addr_len}sf3B"

    def __init__(self, connection, packet):
        self.conn = connection
        self.packet = packet

    def process(self):
        realm_list = self.conn.server.get_realm_list()
        realm_infos = self._get_realm_info_packets(realm_list)
        response = self._get_full_realm_infos(realm_infos, len(realm_list))
        return None, response

    def _get_realm_info_packets(self, realm_list):
        packets = [None] * len(realm_list)
        for index, realm_name in enumerate(realm_list):
            realm = realm_list[realm_name]
            realm_info = self._get_realm_info_packet(realm)
            packets[index] = realm_info
        return b"".join(packets)

    def _get_realm_info_packet(self, realm):
        name_bytes = realm["name"].encode("ascii") + b"\x00"
        address_bytes = realm["address"].encode("ascii") + b"\x00"

        realm_struct_format = RealmlistRequest.REALM_PACKET_FMT.format(
            name_len = len(name_bytes), addr_len = len(address_bytes)
        )
        realm_struct = Struct(realm_struct_format)
        packet = realm_struct.pack(
            0,  # icon ??
            0,  # flags ??
            name_bytes,
            address_bytes,
            realm["population"],
            0,  # num_chars ?
            0,  # timezone ?
            0   # unknown ?
        )
        return packet

    def _get_full_realm_infos(self, realm_infos, num_realms):
        full_packet_size = RealmlistRequest.MIN_RESPONSE_SIZE + len(realm_infos)
        header = RealmlistRequest.RESPONSE_HEADER_BIN.pack(
            LoginOpCodes.REALMLIST.value,
            full_packet_size,
            0,  # unknown
            num_realms
        )
        footer = RealmlistRequest.RESPONSE_FOOTER_BIN.pack(
            0  # unknown
        )
        return header + realm_infos + footer
