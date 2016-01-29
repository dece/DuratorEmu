from struct import Struct
import time

from durator.world.game.spell.constants import SpellId, SPELL_VALUES
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

    # uint16    spell_id
    # uint16    item_id
    # uint16    spell_category
    # uint32    cooldown
    # uint32    cooldown_category
    COOLDOWN_BIN = Struct("<3H2I")

    def __init__(self, player):
        super().__init__(OpCode.SMSG_INITIAL_SPELLS)
        self.player = player
        self._prepare_packet()

    def _prepare_packet(self):
        """ Compute the bytes of the WorldPacket. """
        data = b""

        with self.player.lock:
            num_spells = len(self.player.spells)
            data += self.HEADER_BIN.pack(0, num_spells)

            count = 1
            for spell in self.player.spells:
                data += self.SPELL_BIN.pack(spell.ident, count)
                count += 1

            data += int.to_bytes(num_spells, 2, "little")
            now = int(time.time())
            for spell in self.player.spells:
                values = SPELL_VALUES[SpellId(spell.ident)]
                category = values[0]
                data += self.COOLDOWN_BIN.pack(spell.ident, category, 0, now, 0)

        self.data = data
