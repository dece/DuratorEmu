import unittest

import durator.srp


IDENT    = "IDENT"
SALT     = \
 17462768296609894957082901611113140576623891301766575857231659296666997310951
VERIFIER = \
 60380584250612231381132636201165357654575069546333442709097994879457576481503

SOME_CLIENT_EPH = \
 0x0B242A04170CE90D34E76D78B2D61493F1AEFB7C87E3370381B622E832C92987
SOME_SERVER_EPH = \
 60698480549145741440288951503183065443060075677860685184268433736323767171443

SALT_BYTES = int.to_bytes(SALT, 32, "little")


class TestSrp(unittest.TestCase):

    def test_gen_verifier(self):
        verifier = durator.srp.Srp._gen_verifier(IDENT, IDENT, SALT_BYTES)
        self.assertEquals(verifier, VERIFIER)

    # def test_gen_server_ephemeral(self):
    #     pass

    # def test_gen_session_key(self):
    #     pass

    def test_scramble(self):
        big_a = SOME_CLIENT_EPH
        big_b = SOME_SERVER_EPH
        scramble = durator.srp.Srp._scramble_a_b(big_a, big_b)
        expected = 727196640835373530208271800662769865318063555274
        self.assertEquals(scramble, expected)

    def test_sha1_interleave(self):
        big_int = 1555674156741514756417567416567415647156
        expected = ( b"6\xa0\xf9\xcf\x1f\xe01\x96\xfc\x87\xd7F-"
                     b"\x88\xfd\x9a\xd0\xa5\xe0C\xdb\xdc\xfb\xf7"
                     b"\xf7\x04\x8b\xa8\x12\r/4SjR^7:\x86U" )
        result = durator.srp._sha1_interleave(big_int)
        self.assertEquals(result, expected)

    # def test_gen_client_proof(self):
    #     pass
