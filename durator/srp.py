import hashlib
import os
import random

random.seed()


class Srp(object):

    MODULUS = int("0894B645E89E1535BBDAD5B8B2906505"
                  "30801B18EBFBF5E8FAB3C82872A3E9BB7", 16)
    GENERATOR = 7
    MULTIPLIER = 3

    def __init__(self):
        self.priv_ephemeral = 0
        self._gen_priv_ephemeral()
        self.server_ephemeral = 0

    def _gen_priv_ephemeral(self):
        random_19_bytes = os.urandom(19)
        big_random_int = int.from_bytes(random_19_bytes, "big")
        priv_ephemeral = big_random_int % Srp.MODULUS
        self.priv_ephemeral = priv_ephemeral

    def gen_server_ephemeral(self, verifier):
        big_integer = pow(Srp.GENERATOR, self.priv_ephemeral, Srp.MODULUS)
        ephemeral = (Srp.MULTIPLIER * verifier + big_integer) % Srp.MODULUS
        self.server_ephemeral = ephemeral

    @staticmethod
    def gen_pass_entry(ident, password):
        salt = os.urandom(32)
        verifier = Srp._gen_verifier(ident, password, salt)
        pass_entry = SrpPassEntry(ident, verifier, salt)
        return pass_entry

    @staticmethod
    def _gen_verifier(ident, password, salt):
        logs = ident + ":" + password
        logs_bytes = logs.encode("ascii")
        x_content = salt + logs_bytes
        x_bytes = _sha1(x_content)
        x_int = int.from_bytes(x_bytes, byteorder = "big")
        verifier = pow(Srp.GENERATOR, x_int, Srp.MODULUS)
        return verifier


class SrpPassEntry(object):
    """ A SRP pass entry as stored by the server.

    Attributes:
        ident: str, account name
        verifier: int, computed from account and pass
        salt: bytes, length 32
    """

    def __init__(self, ident, verifier, salt):
        self.ident = ident
        self.verifier = verifier
        self.salt = salt


def _sha1(data):
    hasher = hashlib.sha1(data)
    return hasher.digest()
