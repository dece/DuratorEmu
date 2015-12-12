from enum import Enum
from struct import Struct


class Realm(object):

    REALM_PACKET_FMT = "<IB{name_len}s{addr_len}sf3B"

    def __init__(self, name, address, realm_id):
        self.name = name
        self.address = address
        self.realm_id = realm_id

    def get_state_packet(self, flags, population):
        """ Return a RealmInfo_S packet describing the realm state. It starts
        with a uint8 of its size. """
        name_bytes = self.name.encode("ascii") + b"\x00"
        address_bytes = self.address.encode("ascii") + b"\x00"

        realm_struct_format = Realm.REALM_PACKET_FMT.format(
            name_len = len(name_bytes), addr_len = len(address_bytes)
        )
        realm_struct = Struct(realm_struct_format)
        packet = realm_struct.pack(
            self.realm_id.value,
            flags.value,
            name_bytes,
            address_bytes,
            population.as_float(),
            0,  # num_chars
            0,  # timezone ?
            0   # unknown
        )

        size_bytes = int.to_bytes(len(packet), 1, "little")
        return size_bytes + packet


class RealmId(Enum):
    """ Key in Cfg_Configs.dbc column 1. These are values for build 4125. """

    SERVER0_NORMAL = 0
    SERVER1_PVP    = 1
    SERVER2_NORMAL = 2
    SERVER3_PVP    = 3
    SERVER4_NORMAL = 4
    SERVER5_PVP    = 5
    SERVER6_RP     = 6
    SERVER7_RP     = 7
    SERVER8        = 8  # not present in db


class RealmFlags(Enum):
    """ Flags describing the realm current state. """

    NORMAL  = 0
    LOCKED  = 1
    OFFLINE = 2


class RealmPopulation(Enum):
    """ Represent how crowded a server is (weirdly, sent as a float). """

    LOW     = 0
    AVERAGE = 1
    HIGH    = 2
    FULL    = 3

    def as_float(self):
        return float(self.value)
