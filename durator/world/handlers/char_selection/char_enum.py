from struct import Struct

from durator.world.game.char.character import CharacterEquipSlot
from durator.world.opcodes import OpCode
from durator.world.world_packet import WorldPacket


class CharEnumHandler(object):

    # ulong GUID, string name, uint8 race/class/gender,
    # uint8 skin/face/hairstyle/haircolor/facialhair, uint8 level,
    # uint32 zone, uint32 map, float x/y/z, uint32 guild, uint32 charflags?,
    # uint8 firstlogin, uint32 petdisplay/petlevel/petfamily
    CHAR_FMT = "<Q{name_len}s3B5BB2I3f2IB3I"
    CHAR_EQUIPMENT_BIN = Struct("<IB")

    RESPONSE_HEADER_BIN = Struct("<B")

    def __init__(self, connection, packet):
        self.conn = connection
        self.packet = packet

    def process(self):
        num_chars = 0
        characters_data = []
        for character in self.conn.account.chars:
            character_data = self._get_character_data(character)
            characters_data.append(character_data)
            num_chars += 1
        characters_data = b"".join(characters_data)

        packet = self._get_packet(num_chars, characters_data)
        return None, packet

    def _get_character_data(self, character):
        """ Return the character data needed for this character. It includes a
        lot of general information, one equipment entry per not-bag item, and
        add the first 16-slot bag after that, because why not. """
        name_bytes = character.name.encode("utf8") + b"\x00"
        char_struct_fmt = self.CHAR_FMT.format(name_len = len(name_bytes))
        char_struct = Struct(char_struct_fmt)
        char_data = char_struct.pack(
            character.guid,
            name_bytes,
            character.race,
            character.class_id,
            character.gender,
            character.features.skin,
            character.features.face,
            character.features.hair_style,
            character.features.hair_color,
            character.features.facial_hair,
            character.stats.level,
            character.position.zone_id,
            character.position.map_id,
            character.position.pos_x,
            character.position.pos_y,
            character.position.pos_z,
            0,  # guild
            0,  # char flags?
            0,  # first login
            0,  # pet display
            0,  # pet level
            0   # pet family
        )

        char_equipments = []
        for _ in range( CharacterEquipSlot.HEAD.value
                      , CharacterEquipSlot.TABARD.value + 1 ):
            equipment_data = self.CHAR_EQUIPMENT_BIN.pack(0, 0)
            char_equipments.append(equipment_data)
        first_bag_data = self.CHAR_EQUIPMENT_BIN.pack(0, 0)
        char_equipments.append(first_bag_data)
        char_equipment_data = b"".join(char_equipments)

        return char_data + char_equipment_data

    def _get_packet(self, num_chars, data):
        response_data = self.RESPONSE_HEADER_BIN.pack(num_chars) + data
        packet = WorldPacket(response_data)
        packet.opcode = OpCode.SMSG_CHAR_ENUM
        return packet

