from struct import Struct

from durator.auth.constants import LoginOpCode


class RealmlistRequest(object):
    """ Handle a realm list request (opcode 0x10). """

    MIN_RESPONSE_SIZE = 7

    RESPONSE_HEADER_BIN = Struct("<BHIB")
    RESPONSE_FOOTER_BIN = Struct("<H")
    REALM_PACKET_FMT    = "<IB{name_len}s{addr_len}sf3B"

    def __init__(self, connection, packet):
        self.conn = connection
        self.packet = packet

    def process(self):
        realm_list = self.conn.server.get_realm_list()
        realminfos = self._get_realminfo_packets(realm_list)
        response = self._get_realmlist_packet(realminfos, len(realm_list))
        return None, response

    def _get_realminfo_packets(self, realm_list):
        packets = [None] * len(realm_list)
        for index, realm_name in enumerate(realm_list):
            realminfo = realm_list[realm_name]["packet"]
            packets[index] = realminfo
        return b"".join(packets)

    def _get_realmlist_packet(self, realminfos, num_realms):
        full_packet_size = RealmlistRequest.MIN_RESPONSE_SIZE + len(realminfos)
        header = RealmlistRequest.RESPONSE_HEADER_BIN.pack(
            LoginOpCode.REALMLIST.value,
            full_packet_size,
            0,  # unknown
            num_realms
        )
        footer = RealmlistRequest.RESPONSE_FOOTER_BIN.pack(
            0  # unknown
        )
        return header + realminfos + footer
