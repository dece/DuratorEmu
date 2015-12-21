import unittest

import durator.world.handlers.game.player_login as player_login


GUID       = 0x00000000000DF34B
GUID_MASK  = 7  # 00000111
GUID_BYTES = b"\x4B\xF3\x0D"


class TestUpdateObject(unittest.TestCase):

    def test_pack_guid(self):
        guid_mask, guid_bytes = player_login._pack_guid(GUID)
        self.assertEquals(guid_mask, GUID_MASK)
        self.assertEquals(guid_bytes, GUID_BYTES)
