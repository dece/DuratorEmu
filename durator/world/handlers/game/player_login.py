from struct import Struct

from durator.db.database import db_connection
from durator.world.character import Character
from durator.world.game.object import ObjectType, ObjectDescFlags
from durator.world.game.update_fields import (
    UpdateFieldObject, UpdateFieldUnit, UpdateFieldPlayer )
from durator.world.game.update_object import UpdateType, UpdateObjectBuilder
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
        self.conn.guid = self.PACKET_BIN.unpack(self.packet)[0]
        self.conn.character = self._get_checked_character()
        if self.conn.character is None:
            LOG.warning("Account {} tried to illegally use character {}".format(
                self.conn.account.name, self.conn.guid
            ))
            return self.conn.MAIN_ERROR_STATE, None

        # self.conn.send_packet(self._get_verify_login_packet())
        # self.conn.send_packet(self._get_new_world_packet())
        # self.conn.shared_data["worldport_ack_pending"] = True
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

    # def _get_verify_login_packet(self):
    #     position = self.conn.character.position
    #     response_data = self.WORLD_INFO_BIN.pack(
    #         position.map_id,
    #         position.pos_x,
    #         position.pos_y,
    #         position.pos_z,
    #         position.orientation
    #     )

    #     packet = WorldPacket(response_data)
    #     packet.opcode = OpCode.SMSG_LOGIN_VERIFY_WORLD
    #     return packet

    # def _get_new_world_packet(self):
    #     position = self.conn.character.position
    #     response_data = self.WORLD_INFO_BIN.pack(
    #         position.map_id,
    #         position.pos_x,
    #         position.pos_y,
    #         position.pos_z,
    #         position.orientation
    #     )

    #     packet = WorldPacket(response_data)
    #     packet.opcode = OpCode.SMSG_NEW_WORLD
    #     return packet


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

        update = UpdateObjectBuilder()
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
