from enum import Enum
from struct import Struct


class Realm(object):

    REALM_PACKET_FMT = "<IB{name_len}s{addr_len}sf3B"

    def __init__(self, name, address, game_type):
        self.name = name
        self.address = address
        self.game_type = game_type

    def get_state_packet(self, population):
        """ Return a RealmInfo_S packet describing the realm state. It starts
        with a uint8 of its size. """
        name_bytes = self.name.encode("ascii") + b"\x00"
        address_bytes = self.address.encode("ascii") + b"\x00"

        realm_struct_format = Realm.REALM_PACKET_FMT.format(
            name_len = len(name_bytes), addr_len = len(address_bytes)
        )
        realm_struct = Struct(realm_struct_format)
        packet = realm_struct.pack(
            self.game_type.value,
            0,  # flags
            name_bytes,
            address_bytes,
            population.value,
            0,  # num_chars
            0,  # timezone
            0   # unknown
        )

        size_bytes = int.to_bytes(len(packet), 1, "little")
        return size_bytes + packet


class RealmGameType(Enum):

    NORMAL   = 0
    PVP      = 1
    ROLEPLAY = 6
