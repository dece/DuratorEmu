from struct import Struct

from durator.world.opcodes import OpCode
from durator.world.world_packet import WorldPacket


class InitialSpellsPacket(WorldPacket):
    """ Packet in charge to send spell data at login. """

    # uint8     unk
    # uint16    num_spells
    HEADER_BIN = Struct("<BH")

    # uint16    spell_id
    # uint16    unk
    SPELL_BIN  = Struct("<2H")

    def __init__(self, player):
        super().__init__(OpCode.SMSG_INITIAL_SPELLS)
        self.player = player
        self._prepare_packet()

    def _prepare_packet(self):
        """ Compute the bytes of the WorldPacket. """
        data = b""

        num_spells = len(self.player.spells)
        data += self.HEADER_BIN.pack(0, num_spells)

        for spell in self.player.spells:
            data += self.SPELL_BIN.pack(spell.ident, 0)

        data += int.to_bytes(0, 2, "little")  # no cooldowns

        self.data = data
