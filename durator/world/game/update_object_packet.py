""" Tools for the SMSG_UPDATE_OBJECT (and the compressed counterpart). """

from enum import Enum
import math
from struct import Struct

from durator.world.game.character.defaults import NEW_CHAR_DEFAULTS
from durator.world.game.object.type.base_object import ObjectType
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
        super().__init__(OpCode.SMSG_UPDATE_OBJECT)
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
        data += self.PACKET_PART1_BIN.pack(
            1, 0, self.update_type.value, player.guid, ObjectType.PLAYER.value
        )

        # Assumes no flag for the movement
        movement_struct = Struct(self.PACKET_MOVEMENT_FMT.format())
        data += movement_struct.pack(
            0, 0,
            player.position.x,
            player.position.y,
            player.position.z,
            player.position.o,
            NEW_CHAR_DEFAULTS["speed_walk"],
            NEW_CHAR_DEFAULTS["speed_run"],
            NEW_CHAR_DEFAULTS["speed_run_bw"],
            NEW_CHAR_DEFAULTS["speed_swim"],
            NEW_CHAR_DEFAULTS["speed_swim_bw"],
            NEW_CHAR_DEFAULTS["speed_turn"]
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
        self.update_blocks = {}

    def add(self, field, value):
        """ Add a field and its value to the UpdateBlocks. """
        try:
            field_type = FIELD_TYPE_MAP[field]
        except KeyError:
            LOG.error("No type associated with " + str(field))
            LOG.error("Object not updated.")
            return
        field_struct = self.FIELD_BIN_MAP[field_type]

        field_index = UpdateBlocksBuilder._get_field_index(field)
        self._set_field_mask_bits(field_index, field_struct)
        self._set_field_value(field_index, field_struct, value)

        assert len(self.mask_blocks) < self.HARD_MASK_BLOCKS_LIMIT

    @staticmethod
    def _get_field_index(field):
        if isinstance(field, Enum):
            return field.value
        else:
            return int(field)

    def _set_field_mask_bits(self, field_index, field_struct):
        num_mask_blocks = math.ceil(field_struct.size / 4)
        for index in range(field_index, field_index + num_mask_blocks):
            self._set_field_mask_bit(index)

    def _set_field_mask_bit(self, field_index):
        mask_block_index = field_index // 32
        bit_index = field_index % 32
        while len(self.mask_blocks) < mask_block_index+1:
            self.mask_blocks.append(0)
        self.mask_blocks[mask_block_index] |= 1 << bit_index

    def _set_field_value(self, field_index, field_struct, value):
        update_block = field_struct.pack(value)
        self.update_blocks[field_index] = update_block

    def to_bytes(self):
        """ Return the mask count, the mask and the update blocks as bytes. """
        num_mask_blocks_bytes = int.to_bytes(len(self.mask_blocks), 1, "little")

        mask_blocks = [int.to_bytes(b, 4, "little") for b in self.mask_blocks]
        mask_bytes = b"".join(mask_blocks)

        sorted_blocks = [ self.update_blocks[k]
                          for k in sorted(self.update_blocks.keys()) ]
        update_data = b"".join(sorted_blocks)

        return num_mask_blocks_bytes + mask_bytes + update_data
