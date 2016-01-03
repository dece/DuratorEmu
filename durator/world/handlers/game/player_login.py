from enum import Enum
import math
from struct import Struct

from durator.db.database import db_connection
from durator.world.character import Character
from durator.world.game.update_fields import (
    UpdateFieldObject, UpdateFieldUnit, UpdateFieldPlayer )
from durator.world.game.update_fields_type import (
    UpdateFieldsType, UPDATE_FIELD_TYPE_MAP )
from durator.world.opcodes import OpCode
from durator.world.world_connection_state import WorldConnectionState
from durator.world.world_packet import WorldPacket
from pyshgck.logger import LOG


class UpdateType(Enum):
    """ Determine the UpdateObject packet format. """

    PARTIAL       = 0  # to be confirmed / renamed
    MOVEMENT      = 1
    CREATE_OBJECT = 2
    FAR_OBJECTS   = 3
    NEAR_OBJECTS  = 4


class ObjectType(Enum):
    """ Object type sent in UpdateObject packets, with associated flags. """

    OBJECT         = 0  # 0x01 (object)
    ITEM           = 1  # 0x03 (object, item)
    CONTAINER      = 2  # 0x07 (object, item, container)
    UNIT           = 3  # 0x09 (object, unit)
    PLAYER         = 4  # 0x19 (object, unit, player)
    GAME_OBJECT    = 5  # 0x21 (object, game_object)
    DYNAMIC_OBJECT = 6  # 0x41 (object, dynamic_object)
    CORPSE         = 7  # 0x81 (object, corpse)


class ObjectDescFlags(Enum):
    """ BaseObject descriptors "flags" (field 0x8). """

    OBJECT         = 1 << 0
    ITEM           = 1 << 1
    CONTAINER      = 1 << 2
    UNIT           = 1 << 3
    PLAYER         = 1 << 4
    GAME_OBJECT    = 1 << 5
    DYNAMIC_OBJECT = 1 << 6
    CORPSE         = 1 << 7










class ObjectUpdate(object):

    FIELD_BIN_MAP = {
        UpdateFieldsType.INT32:      Struct("<i"),
        UpdateFieldsType.TWO_INT16:  Struct("<I"),
        UpdateFieldsType.FLOAT:      Struct("<f"),
        UpdateFieldsType.INT64:      Struct("<q"),
        UpdateFieldsType.FOUR_BYTES: Struct("<I")
    }

    def __init__(self):
        self.mask_blocks = []
        self.update_blocks = []

    def add(self, field, value):
        try:
            field_type = UPDATE_FIELD_TYPE_MAP[field]
        except KeyError:
            LOG.error("No type associated with " + str(field))
            LOG.error("Object not updated.")
            return

        field_struct = self.FIELD_BIN_MAP[field_type]
        self._set_field_mask_bits(field, field_struct)

        update_block = field_struct.pack(value)
        self.update_blocks.append(update_block)

    def _set_field_mask_bits(self, field, field_struct):
        num_mask_blocks = math.ceil(field_struct.size / 4)
        for field_value in range(field.value, field.value + num_mask_blocks):
            self._set_field_mask_bit(field_value)

    def _set_field_mask_bit(self, field_value):
        mask_block_index = field_value // 32
        bit_index = field_value % 32
        while len(self.mask_blocks) < mask_block_index+1:
            self.mask_blocks.append(0)
        self.mask_blocks[mask_block_index] |= 1 << bit_index

    def to_bytes(self):
        mask = b"".join(
            [int.to_bytes(block, 4, "little") for block in self.mask_blocks]
        )
        update_data = b"".join(
            self.update_blocks
        )
        return mask + update_data


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
        self.conn.shared_data["worldport_ack_pending"] = True
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
    UPDATE_PART2_BIN    = Struct("<3IQ")

    def _get_update_object_packet(self):
        """ Copy pasted stuff from WoWCore, with a few adaptations for 1.1 """
        char = self.conn.character
        race = char.race
        class_id = char.class_id
        gender = char.gender

        position = char.position

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
            0   # victim GUID
        )

        update = ObjectUpdate()
        update.add(UpdateFieldObject.GUID, self.conn.guid)
        update.add(UpdateFieldObject.TYPE, ( ObjectDescFlags.OBJECT.value |
                                             ObjectDescFlags.UNIT.value |
                                             ObjectDescFlags.PLAYER.value ) )
        update.add(UpdateFieldObject.SCALE_X, 1.0)

        update.add(UpdateFieldUnit.HEALTH, 100)
        update.add(UpdateFieldUnit.POWER_1, 100)
        update.add(UpdateFieldUnit.POWER_2, 100)
        update.add(UpdateFieldUnit.POWER_3, 100)
        update.add(UpdateFieldUnit.POWER_4, 100)
        update.add(UpdateFieldUnit.POWER_5, 100)
        update.add(UpdateFieldUnit.MAX_HEALTH, 100)
        update.add(UpdateFieldUnit.MAX_POWER_1, 100)
        update.add(UpdateFieldUnit.MAX_POWER_2, 100)
        update.add(UpdateFieldUnit.MAX_POWER_3, 100)
        update.add(UpdateFieldUnit.MAX_POWER_4, 100)
        update.add(UpdateFieldUnit.MAX_POWER_5, 100)

        update.add(UpdateFieldUnit.LEVEL, 1)
        update.add(UpdateFieldUnit.FACTION_TEMPLATE, 35)  # or 5 for undead?
        update.add(UpdateFieldUnit.BYTES_0, ( race | (class_id << 8) |
                                              (gender << 16) | (1 << 24) ) )
        update.add(UpdateFieldUnit.FLAGS, 0)

        update.add(UpdateFieldUnit.BASE_ATTACK_TIME, 2000)
        update.add(UpdateFieldUnit.OFFHAND_ATTACK_TIME, 2000)

        update.add(UpdateFieldUnit.BOUNDING_RADIUS, 0.382999)  # undead values
        update.add(UpdateFieldUnit.COMBAT_REACH, 1.500000)

        update.add(UpdateFieldUnit.DISPLAY_ID, 57)
        update.add(UpdateFieldUnit.NATIVE_DISPLAY_ID, 57)
        update.add(UpdateFieldUnit.MOUNT_DISPLAY_ID, 0)

        update.add(UpdateFieldUnit.MIN_DAMAGE, 0)
        update.add(UpdateFieldUnit.MAX_DAMAGE, 0)
        update.add(UpdateFieldUnit.MIN_OFFHAND_DAMAGE, 0)
        update.add(UpdateFieldUnit.MAX_OFFHAND_DAMAGE, 0)

        update.add(UpdateFieldUnit.BYTES_1, 0)  # stand state and stuff

        update.add(UpdateFieldUnit.MOD_CAST_SPEED, 1)

        update.add(UpdateFieldUnit.STAT_0, 0)
        update.add(UpdateFieldUnit.STAT_1, 1)
        update.add(UpdateFieldUnit.STAT_2, 2)
        update.add(UpdateFieldUnit.STAT_3, 3)
        update.add(UpdateFieldUnit.STAT_4, 4)

        update.add(UpdateFieldUnit.RESISTANCE_0, 0)
        update.add(UpdateFieldUnit.RESISTANCE_1, 1)
        update.add(UpdateFieldUnit.RESISTANCE_2, 2)
        update.add(UpdateFieldUnit.RESISTANCE_3, 3)
        update.add(UpdateFieldUnit.RESISTANCE_4, 4)
        update.add(UpdateFieldUnit.RESISTANCE_5, 5)

        update.add(UpdateFieldUnit.BASE_MANA, 1)

        update.add(UpdateFieldUnit.BYTES_2, 0)  # weapons sheathed and stuff

        update.add(UpdateFieldUnit.ATTACK_POWER, 0)
        update.add(UpdateFieldUnit.ATTACK_POWER_MODS, 0)
        update.add(UpdateFieldUnit.RANGED_ATTACK_POWER, 0)
        update.add(UpdateFieldUnit.RANGED_ATTACK_POWER_MODS, 0)

        update.add(UpdateFieldUnit.MIN_RANGED_DAMAGE, 0)
        update.add(UpdateFieldUnit.MAX_RANGED_DAMAGE, 0)

        features = char.features

        update.add(UpdateFieldPlayer.FLAGS, 0)

        player_bytes_1 = ( features.skin |
                           features.face << 8 |
                           features.hair_style << 16 |
                           features.hair_color << 24 )
        player_bytes_2 = ( features.facial_hair |
                           1 << 24 )  # restInfo
        player_bytes_3 = gender

        update.add(UpdateFieldPlayer.BYTES_1, player_bytes_1)
        update.add(UpdateFieldPlayer.BYTES_2, player_bytes_2)
        update.add(UpdateFieldPlayer.BYTES_3, player_bytes_3)

        update.add(UpdateFieldPlayer.EXP, 100)
        update.add(UpdateFieldPlayer.NEXT_LEVEL_XP, 2500)

        update.add(UpdateFieldPlayer.CHARACTER_POINTS_1, 0)
        update.add(UpdateFieldPlayer.CHARACTER_POINTS_2, 2)

        update.add(UpdateFieldPlayer.BLOCK_PERCENTAGE, 4.0)
        update.add(UpdateFieldPlayer.DODGE_PERCENTAGE, 4.0)
        update.add(UpdateFieldPlayer.PARRY_PERCENTAGE, 4.0)
        update.add(UpdateFieldPlayer.CRIT_PERCENTAGE, 4.0)

        update.add(UpdateFieldPlayer.REST_STATE_EXPERIENCE, 200)
        update.add(UpdateFieldPlayer.COINAGE, 1230000)




        # update mask block count, hard limit at 1C
        num_mask_blocks = len(update.mask_blocks)
        if num_mask_blocks >= 0x1C:
            LOG.critical( "Too much update mask blocks ({:X}), "
                          "you probably fucked up something".format(
                num_mask_blocks
            ))
            raise Exception()
        data += int.to_bytes(num_mask_blocks, 1, "little")

        data += update.to_bytes()

        packet = WorldPacket(data)
        packet.opcode = OpCode.SMSG_UPDATE_OBJECT
        return packet
