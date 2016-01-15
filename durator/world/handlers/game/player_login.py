from struct import Struct

from durator.db.database import db_connection
from durator.world.game.char.character_data import CharacterData
from durator.world.game.object.base_object import ObjectType, ObjectDescFlags
from durator.world.game.object.object_fields import (
    ObjectField, UnitField, PlayerField )
from durator.world.game.update_object_packet import (
    UpdateType, UpdateBlocksBuilder )
from durator.world.opcodes import OpCode
from durator.world.world_connection_state import WorldConnectionState
from durator.world.world_packet import WorldPacket
from pyshgck.logger import LOG


WALK_SPEED         = 2.5
RUNNING_SPEED      = 7.0
RUNNING_BACK_SPEED = 2.5
SWIM_SPEED         = 4.7222223
SWIM_BACK_SPEED    = 4.0
TURN_SPEED         = 3.141593


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
        guid = self.PACKET_BIN.unpack(self.packet)[0]
        character_data = self._get_checked_character(guid)
        if character_data is None:
            LOG.warning("Account {} tried to illegally use character {}".format(
                self.conn.account.name, guid
            ))
            return self.conn.MAIN_ERROR_STATE, None

        # Now that we have the character data, spawn a new player object.
        self.conn.guid = guid
        # OBJECT_MANAGER.add_player()

        # Finally, send the packets necessary to let the client get in world.
        self.conn.send_packet(self._get_verify_login_packet())
        self.conn.send_packet(self._get_tutorial_flags_packet())
        self.conn.send_packet(self._get_update_object_packet())

        return WorldConnectionState.IN_WORLD, None

    def _get_checked_character(self, guid):
        """ Get the character data associated to that GUID, but only if this
        character belongs to the connected account, else return None. """
        try:
            character = CharacterData.get(
                CharacterData.guid == guid
                and CharacterData.account == self.conn.account
            )
            return character
        except CharacterData.DoesNotExist:
            return None

    def _get_verify_login_packet(self):
        """ Send the unique (?) SMSG_LOGIN_VERIFY_WORLD packet. """
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

    def _get_tutorial_flags_packet(self):
        """ I agree with myself that I do not want to support tutorials. """
        tutorial_data = int.to_bytes(0xFFFFFFFF, 4, "little") * 8

        packet = WorldPacket(tutorial_data)
        packet.opcode = OpCode.SMSG_TUTORIAL_FLAGS
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
            WALK_SPEED,
            RUNNING_SPEED,
            RUNNING_BACK_SPEED,
            SWIM_SPEED,
            SWIM_BACK_SPEED,
            TURN_SPEED
        )
        data += self.UPDATE_PART2_BIN.pack(
            1,  # is player?
            1,  # attack cycle
            0,  # timer id
            0   # victim GUID
        )

        update = UpdateBlocksBuilder()
        update.add(ObjectField.GUID, self.conn.guid)
        update.add(ObjectField.TYPE, ( ObjectDescFlags.OBJECT.value |
                                             ObjectDescFlags.UNIT.value |
                                             ObjectDescFlags.PLAYER.value ) )
        update.add(ObjectField.SCALE_X, 1.0)

        update.add(UnitField.HEALTH, 100)
        update.add(UnitField.POWER_1, 100)
        update.add(UnitField.POWER_2, 100)
        update.add(UnitField.POWER_3, 100)
        update.add(UnitField.POWER_4, 100)
        update.add(UnitField.POWER_5, 100)
        update.add(UnitField.MAX_HEALTH, 100)
        update.add(UnitField.MAX_POWER_1, 100)
        update.add(UnitField.MAX_POWER_2, 100)
        update.add(UnitField.MAX_POWER_3, 100)
        update.add(UnitField.MAX_POWER_4, 100)
        update.add(UnitField.MAX_POWER_5, 100)

        update.add(UnitField.LEVEL, 1)
        update.add(UnitField.FACTION_TEMPLATE, 35)  # or 5 for undead?
        update.add(UnitField.BYTES_0, ( race | (class_id << 8) |
                                        (gender << 16) | (1 << 24) ) )
        update.add(UnitField.FLAGS, 0)

        update.add(UnitField.BASE_ATTACK_TIME, 2000)
        update.add(UnitField.OFFHAND_ATTACK_TIME, 2000)

        update.add(UnitField.BOUNDING_RADIUS, 0.382999)  # undead values
        update.add(UnitField.COMBAT_REACH, 1.500000)

        update.add(UnitField.DISPLAY_ID, 57)
        update.add(UnitField.NATIVE_DISPLAY_ID, 57)
        update.add(UnitField.MOUNT_DISPLAY_ID, 0)

        update.add(UnitField.MIN_DAMAGE, 0)
        update.add(UnitField.MAX_DAMAGE, 0)
        update.add(UnitField.MIN_OFFHAND_DAMAGE, 0)
        update.add(UnitField.MAX_OFFHAND_DAMAGE, 0)

        update.add(UnitField.BYTES_1, 0)  # stand state and stuff

        update.add(UnitField.MOD_CAST_SPEED, 1)

        update.add(UnitField.STAT_0, 0)
        update.add(UnitField.STAT_1, 1)
        update.add(UnitField.STAT_2, 2)
        update.add(UnitField.STAT_3, 3)
        update.add(UnitField.STAT_4, 4)

        update.add(UnitField.RESISTANCE_0, 0)
        update.add(UnitField.RESISTANCE_1, 1)
        update.add(UnitField.RESISTANCE_2, 2)
        update.add(UnitField.RESISTANCE_3, 3)
        update.add(UnitField.RESISTANCE_4, 4)
        update.add(UnitField.RESISTANCE_5, 5)

        update.add(UnitField.BASE_MANA, 1)

        update.add(UnitField.BYTES_2, 0)  # weapons sheathed and stuff

        update.add(UnitField.ATTACK_POWER, 0)
        update.add(UnitField.ATTACK_POWER_MODS, 0)
        update.add(UnitField.RANGED_ATTACK_POWER, 0)
        update.add(UnitField.RANGED_ATTACK_POWER_MODS, 0)

        update.add(UnitField.MIN_RANGED_DAMAGE, 0)
        update.add(UnitField.MAX_RANGED_DAMAGE, 0)

        features = char.features

        update.add(PlayerField.FLAGS, 0)

        player_bytes_1 = ( features.skin |
                           features.face << 8 |
                           features.hair_style << 16 |
                           features.hair_color << 24 )
        player_bytes_2 = ( features.facial_hair |
                           1 << 24 )  # restInfo
        player_bytes_3 = gender

        update.add(PlayerField.BYTES_1, player_bytes_1)
        update.add(PlayerField.BYTES_2, player_bytes_2)
        update.add(PlayerField.BYTES_3, player_bytes_3)

        update.add(PlayerField.EXP, 100)
        update.add(PlayerField.NEXT_LEVEL_EXP, 2500)

        update.add(PlayerField.CHARACTER_POINTS_1, 0)
        update.add(PlayerField.CHARACTER_POINTS_2, 2)

        update.add(PlayerField.BLOCK_PERCENTAGE, 4.0)
        update.add(PlayerField.DODGE_PERCENTAGE, 4.0)
        update.add(PlayerField.PARRY_PERCENTAGE, 4.0)
        update.add(PlayerField.CRIT_PERCENTAGE, 4.0)

        update.add(PlayerField.REST_STATE_EXP, 200)
        update.add(PlayerField.COINAGE, 1230000)

        # update mask block count, hard limit at 1C
        num_mask_blocks = len(update.mask_blocks)
        if num_mask_blocks >= 0x1C:
            LOG.critical( "Too much update mask blocks ({} > 0x1C), "
                          "you probably fucked up something".format(
                num_mask_blocks
            ))
            raise Exception()
        data += int.to_bytes(num_mask_blocks, 1, "little")

        data += update.to_bytes()

        packet = WorldPacket(data)
        packet.opcode = OpCode.SMSG_UPDATE_OBJECT
        return packet
