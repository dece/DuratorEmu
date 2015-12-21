from enum import Enum
from struct import Struct

from durator.db.database import db_connection
from durator.world.character import Character
from durator.world.opcodes import OpCode
from durator.world.world_connection_state import WorldConnectionState
from durator.world.world_packet import WorldPacket
from pyshgck.logger import LOG


class UpdateType(Enum):

    PARTIAL       = 0  # to be confirmed
    MOVEMENT      = 1
    CREATE_OBJECT = 2
    FAR_OBJECTS   = 3
    NEAR_OBJECTS  = 4


class ObjectType(Enum):

    ITEM           = 1
    CONTAINER      = 2
    UNIT           = 3
    PLAYER         = 4
    GAME_OBJECT    = 5
    DYNAMIC_OBJECT = 6
    CORPSE         = 7


class PlayerLoginHandler(object):
    """ Handle the player entering in world. """

    # We should answer with a validation and a few more informations. Some
    # things that are sent to the client right after on Mangos Classic are:
    # - send server message of the day
    # - send guild message of the day
    # - check if character is dead, then send corpse reclaim timer
    # - set the rest value
    # - set the homebind
    # - possibly send cinematic if it's a first login
    # - set time speed
    # - maybe teleport player back to his homebind
    # - send friend and ignore list
    # - send stuff like water walk, etc
    # - possibly send server imminent shutdown notice

    PACKET_BIN = Struct("<Q")
    WORLD_INFO_BIN = Struct("<I4f")

    def __init__(self, connection, packet):
        self.conn = connection
        self.packet = packet

    @db_connection
    def process(self):
        self.conn.guid = self.PACKET_BIN.unpack(self.packet)[0]
        self.conn.character = self._get_checked_character()
        if self.conn.character is None:
            LOG.warning("Account {} tried to illegally use character {}".format(
                self.conn.account.name, self.conn.guid
            ))
            return self.conn.MAIN_ERROR_STATE, None

        self.conn.send_packet(self._get_verify_login_packet())
        self.conn.send_packet(self._get_new_world_packet())
        self.conn.temp_data["worldport_ack_pending"] = True
        self.conn.send_packet(self._get_update_object_packet())

        return WorldConnectionState.IN_WORLD, None

    def _get_checked_character(self):
        """ Set the connection character to the specified GUID only if this
        character belongs to the connected account, to avoid illegal uses. """
        try:
            character = Character.get(
                Character.guid == self.conn.guid
                and Character.account == self.conn.account
            )
            return character
        except Character.DoesNotExist:
            return None

    def _get_verify_login_packet(self):
        position = self.conn.character.position
        response_data = self.WORLD_INFO_BIN.pack(
            position.map_id,
            position.pos_x,
            position.pos_y,
            position.pos_z,
            position.orientation
        )

        packet = WorldPacket(response_data)
        packet.opcode = OpCode.SMSG_LOGIN_VERIFY_WORLD
        return packet

    def _get_new_world_packet(self):
        position = self.conn.character.position
        response_data = self.WORLD_INFO_BIN.pack(
            position.map_id,
            position.pos_x,
            position.pos_y,
            position.pos_z,
            position.orientation
        )

        packet = WorldPacket(response_data)
        packet.opcode = OpCode.SMSG_NEW_WORLD
        return packet


    UPDATE_PART1_BIN    = Struct("<I2BQB")
    UPDATE_MOVEMENT_BIN = Struct("<2I4f6f")
    UPDATE_PART2_BIN    = Struct("<3IQI")

    def _get_update_object_packet(self):
        position = self.conn.character.position

        # guid_mask, guid_bytes = _pack_guid(self.conn.guid)
        # packed_guid = int.to_bytes(guid_mask, 1, "little") + guid_bytes

        data = b""
        data += self.UPDATE_PART1_BIN.pack(
            1,  # count
            0,  # has transport?
            UpdateType.CREATE_OBJECT.value,  # update type
            self.conn.guid,
            ObjectType.PLAYER.value  # object type
        )
        data += self.UPDATE_MOVEMENT_BIN.pack(
            0,  # movement flags
            0,  # unk?
            position.pos_x,
            position.pos_y,
            position.pos_z,
            position.orientation,
            2.5,  # walkspeed
            7.0,  # runningspeed
            2.5,  # runbackspeed
            4.7222223,  # swimspeed
            4.0,  # swimbackspeed
            3.141593  # turnrate
        )
        data += self.UPDATE_PART2_BIN.pack(
            1,  # is player?
            1,  # attack cycle
            0,  # timer id
            0,  # victim GUID
            0,  # update mask block count
        )

        packet = WorldPacket(data)
        packet.opcode = OpCode.SMSG_UPDATE_OBJECT
        return packet



def _pack_guid(guid):
    guid_all_bytes = int.to_bytes(guid, 8, "little")
    guid_mask = 0
    guid_bytes = b""
    for index, byte in enumerate(guid_all_bytes):
        if byte:
            guid_mask |= 1 << index
            guid_bytes += guid_all_bytes[index:index+1]
    return guid_mask, guid_bytes
