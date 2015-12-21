from enum import Enum
import math
from struct import Struct

from durator.db.database import db_connection
from durator.world.character import Character
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

    UNK            = 0  # 0x01 (object)
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








class UpdateFieldObject(Enum):

    GUID    = 0
    TYPE    = 2
    ENTRY   = 3
    SCALE_X = 4
    PADDING = 5


class UpdateFieldItem(Enum):

    OWNER                = 6
    CONTAINED            = 8
    CREATOR              = 10
    GIFTCREATOR          = 12
    STACK_COUNT          = 14
    DURATION             = 15
    SPELL_CHARGES        = 16
    FLAGS                = 21
    ENCHANTMENT          = 22
    PROPERTY_SEED        = 43
    RANDOM_PROPERTIES_ID = 44
    ITEM_TEXT_ID         = 45
    DURABILITY           = 46
    MAXDURABILITY        = 47


class UpdateFieldContainer(Enum):

    NUM_SLOTS = 48
    PAD       = 49
    SLOT_1    = 50


class UpdateFieldUnit(Enum):

    CHARM                     = 6
    SUMMON                    = 8
    CHARMED_BY                = 10
    SUMMONED_BY               = 12
    CREATED_BY                = 14
    TARGET                    = 16
    PERSUADED                 = 18
    CHANNEL_OBJECT            = 20
    HEALTH                    = 22
    POWER1                    = 23
    POWER2                    = 24
    POWER3                    = 25
    POWER4                    = 26
    POWER5                    = 27
    MAX_HEALTH                = 28
    MAX_POWER1                = 29
    MAX_POWER2                = 30
    MAX_POWER3                = 31
    MAX_POWER4                = 32
    MAX_POWER5                = 33
    LEVEL                     = 34
    FACTION_TEMPLATE          = 35
    BYTES_0                   = 36
    VIRTUAL_ITEM_SLOT_DISPLAY = 37
    VIRTUAL_ITEM_INFO         = 40
    FLAGS                     = 46
    AURA                      = 47
    AURA_FLAGS                = 95
    AURA_LEVELS               = 101
    AURA_APPLICATIONS         = 113
    AURA_STATE                = 125
    BASE_ATTACK_TIME          = 126
    RANGED_ATTACK_TIME        = 128
    BOUNDING_RADIUS           = 129
    COMBAT_REACH              = 130
    DISPLAY_ID                = 131
    NATIVE_DISPLAY_ID         = 132
    MOUNT_DISPLAY_ID          = 133
    MIN_DAMAGE                = 134
    MAX_DAMAGE                = 135
    MIN_OFFHAND_DAMAGE        = 136
    MAX_OFFHAND_DAMAGE        = 137
    BYTES_1                   = 138
    PET_NUMBER                = 139
    PET_NAME_TIMESTAMP        = 140
    PET_EXPERIENCE            = 141
    PET_NEXT_LEVEL_EXP        = 142
    DYNAMIC_FLAGS             = 143
    CHANNEL_SPELL             = 144
    MOD_CAST_SPEED            = 145
    CREATED_BY_SPELL          = 146
    NPC_FLAGS                 = 147
    NPC_EMOTESTATE            = 148
    TRAINING_POINTS           = 149
    STAT0                     = 150
    STAT1                     = 151
    STAT2                     = 152
    STAT3                     = 153
    STAT4                     = 154
    RESISTANCES               = 155
    BASE_MANA                 = 162
    BASE_HEALTH               = 163
    BYTES_2                   = 164
    ATTACK_POWER              = 165
    ATTACK_POWER_MODS         = 166
    ATTACK_POWER_MULT         = 167
    RANGED_ATTACK_POWER       = 168
    RANGED_ATTACK_POWER_MODS  = 169
    RANGED_ATTACK_POWER_MULT  = 170
    MIN_RANGED_DAMAGE         = 171
    MAX_RANGED_DAMAGE         = 172
    POWER_COST_MODIFIER       = 173
    POWER_COST_MULTIPLIER     = 180
    PADDING                   = 187


class UpdateFieldsType(Enum):

    INT32 = 1  # 4
    INT64 = 2  # 8
    FLOAT = 3  # 4


UPDATE_FIELD_TYPE_MAP = {
    UpdateFieldObject.GUID:    UpdateFieldsType.INT64,
    UpdateFieldObject.TYPE:    UpdateFieldsType.INT32,
    UpdateFieldObject.SCALE_X: UpdateFieldsType.FLOAT,
    UpdateFieldUnit.HEALTH:    UpdateFieldsType.INT32
}


class ObjectUpdate(object):

    FIELD_BIN_MAP = {
        UpdateFieldsType.INT32: Struct("<I"),
        UpdateFieldsType.INT64: Struct("<Q"),
        UpdateFieldsType.FLOAT: Struct("<f")
    }

    def __init__(self):
        self.mask_blocks = []
        self.update_blocks = []

    def add(self, field, value):
        try:
            field_type = UPDATE_FIELD_TYPE_MAP[field]
        except KeyError as exc:
            LOG.error("No type associated with " + str(field) + ": " + str(exc))
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
        mask_block_index = field_value // 8
        bit_index = field_value % 8
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
    UPDATE_PART2_BIN    = Struct("<3IQB")
    UPDATE_UPDATE_MASK_BIN    = Struct("<IQIf")

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
            0,  # update mask block count, hard limit at 1C
        )
        data += self.UPDATE_UPDATE_MASK_BIN.pack(
            0x15,  # mask, 00010101
            self.conn.guid,
            ( ObjectDescFlags.OBJECT.value |
              ObjectDescFlags.UNIT.value |
              ObjectDescFlags.PLAYER.value ),
            1.0
        )


        packet = WorldPacket(data)
        packet.opcode = OpCode.SMSG_UPDATE_OBJECT
        return packet
