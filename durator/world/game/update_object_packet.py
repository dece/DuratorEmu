""" Tools for the SMSG_UPDATE_OBJECT (and the compressed counterpart). """

from enum import Enum
import math
from struct import Struct

from durator.world.game.object_fields_type import FieldsType, FIELD_TYPE_MAP
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

    # uint32  count
    # uint8   bool hasTransport (?)
    # uint8   UPDATE_TYPE
    # uint64  guid
    # uint8   OBJECT_TYPE
    PACKET_PART1_BIN    = Struct("<I2BQB")

    # uint32    flags
    # uint32    unk
    # float[4]  position+ori
    # float[6]  speeds (walk, run, bw, swim, swim bw, turn)
    # may be more complete with some flags
    PACKET_MOVEMENT_FMT = Struct("<2I4f6f")

    # uint32  isPlayer ? 1 : 0
    # uint32  attack cycle
    # uint32  timer ID
    # uint64  victim guid
    PACKET_PART2_BIN    = Struct("<3IQ")

    def __init__(self, data = None):
        super().__init__(self, data)
        self.opcode = OpCode.SMSG_UPDATE_OBJECT

        self.blocks_builder = UpdateBlocksBuilder()

    def add_field(self, field, value):
        self.blocks_builder.add(field, value)

    def create_data(self):
        """ Create binary data from the packet information.
        Required to call to_bytes. """
        update_blocks = self.blocks_builder.to_bytes()
        # TODO complete
        self.data = update_blocks


class UpdateBlocksBuilder(object):
    """ Create the UpdateBlocks part of an UpdateObject packet. """

    FIELD_BIN_MAP = {
        FieldsType.INT32:      Struct("<i"),
        FieldsType.TWO_INT16:  Struct("<I"),
        FieldsType.FLOAT:      Struct("<f"),
        FieldsType.INT64:      Struct("<q"),
        FieldsType.FOUR_BYTES: Struct("<I")
    }

    def __init__(self):
        self.mask_blocks = []
        self.update_blocks = []

    def add(self, field, value):
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


class PlayerSpawner(UpdateBlocksBuilder):
    """ This builder is used to send the world-entering UpdateObject packet.
    Probably a temporary solution until I have a better update object system.
    """

    def __init__(self, character):
        super().__init__(self)
        self.character = character

        # self._prepare_player_values()

