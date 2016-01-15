from struct import Struct

from durator.db.database import db_connection
from durator.world.game.char.character import CharacterData
from durator.world.game.object import ObjectType, ObjectDescFlags
from durator.world.game.object_fields import FieldObject, FieldUnit, FieldPlayer
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
        update.add(FieldObject.GUID, self.conn.guid)
        update.add(FieldObject.TYPE, ( ObjectDescFlags.OBJECT.value |
                                             ObjectDescFlags.UNIT.value |
                                             ObjectDescFlags.PLAYER.value ) )
        update.add(FieldObject.SCALE_X, 1.0)

        update.add(FieldUnit.HEALTH, 100)
        update.add(FieldUnit.POWER_1, 100)
        update.add(FieldUnit.POWER_2, 100)
        update.add(FieldUnit.POWER_3, 100)
        update.add(FieldUnit.POWER_4, 100)
        update.add(FieldUnit.POWER_5, 100)
        update.add(FieldUnit.MAX_HEALTH, 100)
        update.add(FieldUnit.MAX_POWER_1, 100)
        update.add(FieldUnit.MAX_POWER_2, 100)
        update.add(FieldUnit.MAX_POWER_3, 100)
        update.add(FieldUnit.MAX_POWER_4, 100)
        update.add(FieldUnit.MAX_POWER_5, 100)

        update.add(FieldUnit.LEVEL, 1)
        update.add(FieldUnit.FACTION_TEMPLATE, 35)  # or 5 for undead?
        update.add(FieldUnit.BYTES_0, ( race | (class_id << 8) |
                                        (gender << 16) | (1 << 24) ) )
        update.add(FieldUnit.FLAGS, 0)

        update.add(FieldUnit.BASE_ATTACK_TIME, 2000)
        update.add(FieldUnit.OFFHAND_ATTACK_TIME, 2000)

        update.add(FieldUnit.BOUNDING_RADIUS, 0.382999)  # undead values
        update.add(FieldUnit.COMBAT_REACH, 1.500000)

        update.add(FieldUnit.DISPLAY_ID, 57)
        update.add(FieldUnit.NATIVE_DISPLAY_ID, 57)
        update.add(FieldUnit.MOUNT_DISPLAY_ID, 0)

        update.add(FieldUnit.MIN_DAMAGE, 0)
        update.add(FieldUnit.MAX_DAMAGE, 0)
        update.add(FieldUnit.MIN_OFFHAND_DAMAGE, 0)
        update.add(FieldUnit.MAX_OFFHAND_DAMAGE, 0)

        update.add(FieldUnit.BYTES_1, 0)  # stand state and stuff

        update.add(FieldUnit.MOD_CAST_SPEED, 1)

        update.add(FieldUnit.STAT_0, 0)
        update.add(FieldUnit.STAT_1, 1)
        update.add(FieldUnit.STAT_2, 2)
        update.add(FieldUnit.STAT_3, 3)
        update.add(FieldUnit.STAT_4, 4)

        update.add(FieldUnit.RESISTANCE_0, 0)
        update.add(FieldUnit.RESISTANCE_1, 1)
        update.add(FieldUnit.RESISTANCE_2, 2)
        update.add(FieldUnit.RESISTANCE_3, 3)
        update.add(FieldUnit.RESISTANCE_4, 4)
        update.add(FieldUnit.RESISTANCE_5, 5)

        update.add(FieldUnit.BASE_MANA, 1)

        update.add(FieldUnit.BYTES_2, 0)  # weapons sheathed and stuff

        update.add(FieldUnit.ATTACK_POWER, 0)
        update.add(FieldUnit.ATTACK_POWER_MODS, 0)
        update.add(FieldUnit.RANGED_ATTACK_POWER, 0)
        update.add(FieldUnit.RANGED_ATTACK_POWER_MODS, 0)

        update.add(FieldUnit.MIN_RANGED_DAMAGE, 0)
        update.add(FieldUnit.MAX_RANGED_DAMAGE, 0)

        features = char.features

        update.add(FieldPlayer.FLAGS, 0)

        player_bytes_1 = ( features.skin |
                           features.face << 8 |
                           features.hair_style << 16 |
                           features.hair_color << 24 )
        player_bytes_2 = ( features.facial_hair |
                           1 << 24 )  # restInfo
        player_bytes_3 = gender

        update.add(FieldPlayer.BYTES_1, player_bytes_1)
        update.add(FieldPlayer.BYTES_2, player_bytes_2)
        update.add(FieldPlayer.BYTES_3, player_bytes_3)

        update.add(FieldPlayer.EXP, 100)
        update.add(FieldPlayer.NEXT_LEVEL_EXP, 2500)

        update.add(FieldPlayer.CHARACTER_POINTS_1, 0)
        update.add(FieldPlayer.CHARACTER_POINTS_2, 2)

        update.add(FieldPlayer.BLOCK_PERCENTAGE, 4.0)
        update.add(FieldPlayer.DODGE_PERCENTAGE, 4.0)
        update.add(FieldPlayer.PARRY_PERCENTAGE, 4.0)
        update.add(FieldPlayer.CRIT_PERCENTAGE, 4.0)

        update.add(FieldPlayer.REST_STATE_EXP, 200)
        update.add(FieldPlayer.COINAGE, 1230000)

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
