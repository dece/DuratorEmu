""" Tools for the SMSG_UPDATE_OBJECT (and the compressed counterpart). """

from enum import Enum
import math
from struct import Struct

from durator.world.game.char.constants import NEW_CHAR_CONSTS
from durator.world.game.object.base_object import ObjectType
from durator.world.game.object.object_fields import (
    ObjectField, UnitField, PlayerField )
from durator.world.game.object.object_fields_type import (
    FieldType, FIELD_TYPE_MAP )
from durator.world.opcodes import OpCode
from durator.world.world_packet import WorldPacket
from pyshgck.logger import LOG


class UpdateType(Enum):
    """ Determine the UpdateObject packet format. """

    PARTIAL       = 0
    MOVEMENT      = 1
    CREATE_OBJECT = 2
    FAR_OBJECTS   = 3
    NEAR_OBJECTS  = 4


class UpdateObjectPacket(WorldPacket):
    """ WIP """

    UPDATE_TYPES_WITH_FIELDS = ( UpdateType.PARTIAL
                               , UpdateType.MOVEMENT
                               , UpdateType.CREATE_OBJECT )

    # uint32  count
    # uint8   bool hasTransport (?)
    # uint8   UPDATE_TYPE
    # uint64  guid
    # uint8   OBJECT_TYPE
    PACKET_PART1_BIN = Struct("<I2BQB")

    # uint32    flags
    # uint32    unk
    # float[4]  position+ori
    # float[6]  speeds (walk, run, bw, swim, swim bw, turn)
    # may be more complete with some flags
    PACKET_MOVEMENT_FMT = "<2I4f6f"

    # uint32  isPlayer ? 1 : 0
    # uint32  attack cycle
    # uint32  timer ID
    # uint64  victim guid
    PACKET_PART2_BIN = Struct("<3IQ")

    def __init__(self, update_type, update_infos):
        super().__init__(data = None)
        self.opcode = OpCode.SMSG_UPDATE_OBJECT
        self.update_type = update_type
        self.update_infos = update_infos

        if self.update_type != UpdateType.CREATE_OBJECT:
            raise NotImplementedError()

        self.has_fields = self.update_type in self.UPDATE_TYPES_WITH_FIELDS
        self.blocks_builder = UpdateBlocksBuilder() if self.has_fields else None

    def add_field(self, field, value):
        """ If this update packet can hold update fields, add it. """
        if not self.has_fields:
            LOG.error("Tried to add an update field to a wrong update packet.")
            return
        self.blocks_builder.add(field, value)

    def to_socket(self, session_cipher = None):
        """ WIP, this stuff still shouldn't be hardcoded """
        data = b""

        # The update_infos dict should contain the player field at least for
        # type 2 updates, and maybe some others.
        player = self.update_infos["player"]
        guid = player.get(ObjectField.GUID)
        data += self.PACKET_PART1_BIN.pack(
            1, 0, self.update_type.value, guid, ObjectType.PLAYER.value
        )

        # Assumes no flag for the movement
        movement_struct = Struct(self.PACKET_MOVEMENT_FMT.format())
        data += movement_struct.pack(
            0, 0,
            player.coords["x"],
            player.coords["y"],
            player.coords["z"],
            player.coords["o"],
            NEW_CHAR_CONSTS["speed_walk"],
            NEW_CHAR_CONSTS["speed_run"],
            NEW_CHAR_CONSTS["speed_run_bw"],
            NEW_CHAR_CONSTS["speed_swim"],
            NEW_CHAR_CONSTS["speed_swim_bw"],
            NEW_CHAR_CONSTS["speed_turn"]
        )

        data += self.PACKET_PART2_BIN.pack(1, 1, 0, 0)

        data += self.blocks_builder.to_bytes()

        self.data = data
        return super().to_socket(session_cipher)


class UpdateBlocksBuilder(object):
    """ Create the UpdateBlocks part of an UpdateObject packet. """

    FIELD_BIN_MAP = {
        FieldType.INT32:      Struct("<i"),
        FieldType.TWO_INT16:  Struct("<I"),
        FieldType.FLOAT:      Struct("<f"),
        FieldType.INT64:      Struct("<q"),
        FieldType.FOUR_BYTES: Struct("<I")
    }

    HARD_MASK_BLOCKS_LIMIT = 0x1C

    def __init__(self):
        self.mask_blocks = []
        self.update_blocks = []

    def add(self, field, value):
        """ Add a field and its value to the UpdateBlocks. """
        try:
            field_type = FIELD_TYPE_MAP[field]
        except KeyError:
            LOG.error("No type associated with " + str(field))
            LOG.error("Object not updated.")
            return

        field_struct = self.FIELD_BIN_MAP[field_type]
        self._set_field_mask_bits(field, field_struct)

        update_block = field_struct.pack(value)
        self.update_blocks.append(update_block)

        num_mask_blocks = len(self.mask_blocks)
        if num_mask_blocks >= self.HARD_MASK_BLOCKS_LIMIT:
            LOG.critical("Too much update mask blocks ({} >= {})".format(
                num_mask_blocks, self.HARD_MASK_BLOCKS_LIMIT
            ))
            raise Exception()

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
        """ Return the mask count, the mask and the update blocks as bytes. """
        num_mask_blocks_bytes = int.to_bytes(len(self.mask_blocks), 1, "little")
        mask_blocks = [int.to_bytes(b, 4, "little") for b in self.mask_blocks]
        mask_bytes = b"".join(mask_blocks)
        update_data = b"".join(self.update_blocks)
        return num_mask_blocks_bytes + mask_bytes + update_data





# These values are enough to let the client make the player show in world.
# There may be a lot of superfluous values but well...
PLAYER_SPAWN_FIELDS = [
    ObjectField.GUID,
    ObjectField.TYPE,
    ObjectField.SCALE_X,
    UnitField.HEALTH,
    UnitField.POWER_1,
    UnitField.POWER_2,
    UnitField.POWER_3,
    UnitField.POWER_4,
    UnitField.POWER_5,
    UnitField.MAX_HEALTH,
    UnitField.MAX_POWER_1,
    UnitField.MAX_POWER_2,
    UnitField.MAX_POWER_3,
    UnitField.MAX_POWER_4,
    UnitField.MAX_POWER_5,
    UnitField.LEVEL,
    UnitField.FACTION_TEMPLATE,
    UnitField.BYTES_0,
    UnitField.FLAGS,
    UnitField.BASE_ATTACK_TIME,
    UnitField.OFFHAND_ATTACK_TIME,
    UnitField.BOUNDING_RADIUS,
    UnitField.COMBAT_REACH,
    UnitField.DISPLAY_ID,
    UnitField.NATIVE_DISPLAY_ID,
    UnitField.MOUNT_DISPLAY_ID,
    UnitField.MIN_DAMAGE,
    UnitField.MAX_DAMAGE,
    UnitField.MIN_OFFHAND_DAMAGE,
    UnitField.MAX_OFFHAND_DAMAGE,
    UnitField.BYTES_1,
    UnitField.MOD_CAST_SPEED,
    UnitField.STAT_0,
    UnitField.STAT_1,
    UnitField.STAT_2,
    UnitField.STAT_3,
    UnitField.STAT_4,
    UnitField.RESISTANCE_0,
    UnitField.RESISTANCE_1,
    UnitField.RESISTANCE_2,
    UnitField.RESISTANCE_3,
    UnitField.RESISTANCE_4,
    UnitField.RESISTANCE_5,
    UnitField.BASE_MANA,
    UnitField.BYTES_2,
    UnitField.ATTACK_POWER,
    UnitField.ATTACK_POWER_MODS,
    UnitField.RANGED_ATTACK_POWER,
    UnitField.RANGED_ATTACK_POWER_MODS,
    UnitField.MIN_RANGED_DAMAGE,
    UnitField.MAX_RANGED_DAMAGE,
    PlayerField.FLAGS,
    PlayerField.BYTES_1,
    PlayerField.BYTES_2,
    PlayerField.BYTES_3,
    PlayerField.EXP,
    PlayerField.NEXT_LEVEL_EXP,
    PlayerField.CHARACTER_POINTS_1,
    PlayerField.CHARACTER_POINTS_2,
    PlayerField.BLOCK_PERCENTAGE,
    PlayerField.DODGE_PERCENTAGE,
    PlayerField.PARRY_PERCENTAGE,
    PlayerField.CRIT_PERCENTAGE,
    PlayerField.REST_STATE_EXP,
    PlayerField.COINAGE
]


class PlayerSpawnPacket(UpdateObjectPacket):
    """ This specific UpdateObjectPacket is used to let the player spawn.
    May be a temporary solution until I have a better update object system.
    """

    def __init__(self, player):
        update_infos = { "player": player }
        super().__init__(UpdateType.CREATE_OBJECT, update_infos)
        self.player = player

        self._add_required_fields()

    def _add_required_fields(self):
        for required_field in PLAYER_SPAWN_FIELDS:
            value = self.player.get(required_field)
            if value is None:
                LOG.error("A required field for player spawning is not set.")
                LOG.error(str(required_field))
                continue
            self.add_field(required_field, value)
