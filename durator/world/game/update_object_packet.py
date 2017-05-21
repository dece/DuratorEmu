""" Tools for the SMSG_UPDATE_OBJECT (and the compressed counterpart). """

from enum import Enum
import math
from struct import Struct

from durator.world.game.object.object_fields import ObjectField
from durator.world.game.object.object_fields_type import (
    FieldType, FIELD_TYPE_MAP )
from durator.world.game.object.type.base_object import ObjectTypeFlags
from durator.world.game.object.type.unit import DEFAULT_SPEEDS
from durator.world.opcodes import OpCode
from durator.world.world_packet import WorldPacket
from durator.common.log import LOG


class UpdateType(Enum):
    """ Determine the UpdateObject packet format. """

    PARTIAL       = 0
    MOVEMENT      = 1
    CREATE_OBJECT = 2
    FAR_OBJECTS   = 3
    NEAR_OBJECTS  = 4


class UpdateObjectPacket(WorldPacket):
    """ Handle the creation of update packets. It can handle object fields
    update and movement update.

    The update_infos dict contains the most values of interest. Some elements
    must be provided for some update types only:
    - unit: Unit object that this packet concerns. Always provide it.
    - is_player: boolean about whether or not this packet concerns
        the destination player or another unit. Provide it for CREATE_OBJECT.
    """

    TYPES_WITH_OBJECT_TYPE = ( UpdateType.CREATE_OBJECT, )
    TYPES_WITH_MOVEMENT = ( UpdateType.MOVEMENT
                          , UpdateType.CREATE_OBJECT )
    TYPES_WITH_MISC = ( UpdateType.CREATE_OBJECT, )
    TYPES_WITH_FIELDS = ( UpdateType.PARTIAL   # ?
                        , UpdateType.MOVEMENT  # ?
                        , UpdateType.CREATE_OBJECT )

    IMPLEMENTED_TYPES = ( UpdateType.MOVEMENT
                        , UpdateType.CREATE_OBJECT )

    # - uint32  count
    # - uint8   bool hasTransport (?)
    # - uint8   UpdateType
    # - uint64  guid
    PACKET_HEADER_BIN = Struct("<I2BQ")

    # - uint8   ObjectType
    PACKET_OBJECT_TYPE_BIN = Struct("<B")

    # - float       speed_walk
    # - float       speed_run
    # - float       speed_run_bw
    # - float       speed_swim
    # - float       speed_swim_bw
    # - float       speed_turn
    #     if movement.flags & 0x00400000
    #     more stuff
    PACKET_SPEED_BIN = Struct("<6f")

    # - uint32  isPlayer ? 1 : 0
    # - uint32  attack cycle
    # - uint32  timer ID
    # - uint64  victim guid
    PACKET_MISC_BIN = Struct("<3IQ")

    def __init__(self, update_type, update_infos):
        if update_type not in self.IMPLEMENTED_TYPES:
            raise NotImplementedError(str(update_type))

        super().__init__(OpCode.SMSG_UPDATE_OBJECT)
        self.update_type = update_type
        self.update_infos = update_infos

        if self.has_fields():
            self.blocks_builder = UpdateBlocksBuilder()

    def has_fields(self):
        return self.update_type in self.TYPES_WITH_FIELDS

    def add_field(self, field, value):
        """ If this update packet can hold update fields, add it. """
        if not self.has_fields:
            LOG.error("Tried to add an update field to a wrong update packet.")
            return
        self.blocks_builder.add(field, value)

    def to_socket(self, session_cipher = None):
        """ Prepare the bytes to be sent to clients.  """
        base_object = self.update_infos["object"]
        data = b""

        data += self.PACKET_HEADER_BIN.pack(
            1,  # we only send one batch of update values at a time for now
            int(False),
            self.update_type.value,
            base_object.guid
        )

        if self.update_type in self.TYPES_WITH_OBJECT_TYPE:
            data += self.PACKET_OBJECT_TYPE_BIN.pack(base_object.type.value)

        if self.update_type in self.TYPES_WITH_MOVEMENT:
            with base_object.lock:
                # Only objects with movement (= Units and Players) in there.
                object_type_value = base_object.get(ObjectField.TYPE)
                assert object_type_value & ObjectTypeFlags.UNIT.value

                movement_bytes = base_object.movement.to_bytes()
            data += movement_bytes
            data += self.PACKET_SPEED_BIN.pack(
                DEFAULT_SPEEDS["walk"],
                DEFAULT_SPEEDS["run"],
                DEFAULT_SPEEDS["run_bw"],
                DEFAULT_SPEEDS["swim"],
                DEFAULT_SPEEDS["swim_bw"],
                DEFAULT_SPEEDS["turn"]
            )

        if self.update_type in self.TYPES_WITH_MISC:
            data += self.PACKET_MISC_BIN.pack(
                int(self.update_infos["is_player"]),
                1,
                0,
                0
            )

        if self.update_type in self.TYPES_WITH_FIELDS:
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
