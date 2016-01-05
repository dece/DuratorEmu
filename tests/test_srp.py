import unittest

import durator.auth.srp as srp
import durator.common.crypto.sha1 as sha1


IDENT           = "IDENT"
SALT            = \
 17462768296609894957082901611113140576623891301766575857231659296666997310951
VERIFIER        = \
 60380584250612231381132636201165357654575069546333442709097994879457576481503
SOME_CLIENT_EPH = \
 5039337812361797701765812379987240212630060872944935401672217738755319605639
SOME_SERVER_EPH = \
 60698480549145741440288951503183065443060075677860685184268433736323767171443
SCRAMBLED_EPHS  = \
 727196640835373530208271800662769865318063555274


class TestSrp(unittest.TestCase):

    def test_generate_verifier(self):
        salt_bytes = int.to_bytes(SALT, 32, "little")
        verifier = srp.Srp._generate_verifier(IDENT, IDENT, salt_bytes)
        self.assertEquals(verifier, VERIFIER)

    def test_scramble(self):
        big_a = SOME_CLIENT_EPH
        big_b = SOME_SERVER_EPH
        scramble = srp.Srp._scramble_a_b(big_a, big_b)
        self.assertEquals(scramble, SCRAMBLED_EPHS)

    def test_sha1_interleave(self):
        big_int = 1555674156741514756417567416567415647156
        expected = \
            b"6\xa0\xf9\xcf\x1f\xe01\x96\xfc\x87\xd7F-\x88\xfd\x9a\xd0\xa5" \
            b"\xe0C\xdb\xdc\xfb\xf7\xf7\x04\x8b\xa8\x12\r/4SjR^7:\x86U"
        result = sha1.sha1_interleave(big_int)
        self.assertEquals(result, expected)
