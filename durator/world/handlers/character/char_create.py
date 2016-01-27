from enum import Enum
import io
from struct import Struct

from durator.world.game.character.manager import CharacterManager
from durator.world.game.character.constants import (
    CharacterRace, CharacterClass, CharacterGender )
from durator.world.opcodes import OpCode
from durator.world.world_packet import WorldPacket
from pyshgck.bin import read_cstring, read_struct
from pyshgck.logger import LOG


class CharCreateResponseCode(Enum):

    SUCCESS             = 0x2D
    ERROR               = 0x2E
    FAILED              = 0x2F
    NAME_IN_USE         = 0x30
    SERVER_LIMIT        = 0x33
    ACCOUNT_LIMIT       = 0x34


class CharCreateHandler(object):

    PACKET_CHAR_BIN = Struct("<9B")
    RESPONSE_BIN = Struct("<B")

    def __init__(self, connection, packet):
        self.conn = connection
        self.packet = packet

        self.char_name = ""
        self.char_race = None
        self.char_class = None
        self.char_gender = None
        self.char_features = None
        self.unk_value = 0

    def process(self):
        self._parse_packet(self.packet)

        char_values = {
            "name": self.char_name,
            "race": self.char_race,
            "class": self.char_class,
            "gender": self.char_gender,
            "features": {
                "skin": self.char_features[0],
                "face": self.char_features[1],
                "hair_style": self.char_features[2],
                "hair_color": self.char_features[3],
                "facial_hair": self.char_features[4]
            }
        }
        manager_code = CharacterManager.create_character(
            self.conn.account, char_values
        )

        packet = self._get_response_packet(manager_code)
        return None, packet

    def _parse_packet(self, packet):
        packet_io = io.BytesIO(packet)
        char_name_bytes = read_cstring(packet_io, 0)
        self.char_name = char_name_bytes.decode("utf8")
        char_data = read_struct(packet_io, self.PACKET_CHAR_BIN)

        self.char_race = CharacterRace(char_data[0])
        self.char_class = CharacterClass(char_data[1])
        self.char_gender = CharacterGender(char_data[2])
        self.char_features = char_data[3:8]
        self.unk_value = char_data[8]

    def _get_response_packet(self, manager_code):
        response_code = {
            0: CharCreateResponseCode.SUCCESS,
            1: CharCreateResponseCode.FAILED,
            2: CharCreateResponseCode.NAME_IN_USE,
            3: CharCreateResponseCode.ERROR
        }.get(manager_code, 1)
        LOG.debug("Character creation status: " + str(response_code))

        response_data = self.RESPONSE_BIN.pack(response_code.value)
        return WorldPacket(OpCode.SMSG_CHAR_CREATE, response_data)
