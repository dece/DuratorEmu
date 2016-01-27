from enum import Enum
from struct import Struct

from durator.world.game.character.manager import CharacterManager
from durator.world.opcodes import OpCode
from durator.world.world_packet import WorldPacket
from pyshgck.logger import LOG


class CharDeleteResponseCode(Enum):

    SUCCESS = 0x38
    FAILED  = 0x39


class CharDeleteHandler(object):

    PACKET_BIN   = Struct("<Q")
    RESPONSE_BIN = Struct("<B")

    def __init__(self, connection, packet):
        self.conn = connection
        self.packet = packet

    def process(self):
        guid = self.PACKET_BIN.unpack(self.packet)[0]
        manager_code = CharacterManager.delete_char(guid)
        packet = self._get_response_packet(manager_code)
        return None, packet

    def _get_response_packet(self, manager_code):
        response_code = {
            0: CharDeleteResponseCode.SUCCESS,
            1: CharDeleteResponseCode.FAILED
        }.get(manager_code, 1)
        LOG.debug("Character creation status: " + str(response_code.name))

        response_data = self.RESPONSE_BIN.pack(response_code.value)
        return WorldPacket(OpCode.SMSG_CHAR_DELETE, response_data)
