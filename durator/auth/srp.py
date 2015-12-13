""" Clunky implementation of the SRP login process.

Details on SRP are available here: https://www.ietf.org/rfc/rfc2945.txt
WoW use it with fixed modulus and generator values.
"""

import os

from durator.common.crypto import sha1, sha1_interleave


class Srp(object):
    """ SRP login manager

    Attributes:
        priv_ephemeral: big private integer
        server_ephemeral: big public integer
        session_key: 40 bytes computed secretly by client and server
        client_proof: 20 bytes proof computed, should match client's proof
        server_proof: 20 bytes proof hash
    """

    MODULUS    = \
        0x894B645E89E1535BBDAD5B8B290650530801B18EBFBF5E8FAB3C82872A3E9BB7
    GENERATOR  = 7
    MULTIPLIER = 3

    def __init__(self):
        self.priv_ephemeral = 0
        self._generate_priv_ephemeral()
        self.server_ephemeral = 0
        self.session_key = b""
        self.client_proof = b""
        self.server_proof = b""

    def _generate_priv_ephemeral(self):
        random_19_bytes = os.urandom(19)
        big_random_int = int.from_bytes(random_19_bytes, "little")
        priv_ephemeral = big_random_int % Srp.MODULUS
        self.priv_ephemeral = priv_ephemeral

    def generate_server_ephemeral(self, verifier):
        big_integer = pow(Srp.GENERATOR, self.priv_ephemeral, Srp.MODULUS)
        ephemeral = (Srp.MULTIPLIER * verifier + big_integer) % Srp.MODULUS
        self.server_ephemeral = ephemeral

    def generate_session_key(self, client_eph, verifier):
        assert self.server_ephemeral
        scramble = Srp._scramble_a_b(client_eph, self.server_ephemeral)
        pow_verifier = pow(verifier, scramble, Srp.MODULUS)
        pow_verifier *= client_eph
        to_interleave = pow(pow_verifier, self.priv_ephemeral, Srp.MODULUS)
        self.session_key = sha1_interleave(to_interleave)

    @staticmethod
    def _scramble_a_b(big_int_a, big_int_b):
        a_bytes = int.to_bytes(big_int_a, 32, "little")
        b_bytes = int.to_bytes(big_int_b, 32, "little")
        scramble_hash = sha1(a_bytes + b_bytes)
        scramble = int.from_bytes(scramble_hash, "little")
        return scramble

    def generate_client_proof(self, client_ephemeral, account):
        assert self.server_ephemeral
        assert self.session_key
        modulus_bytes = int.to_bytes(Srp.MODULUS, 32, "little").rstrip(b"\x00")
        modulus_hash = sha1(modulus_bytes)
        gen_bytes = int.to_bytes(Srp.GENERATOR, 32, "little").rstrip(b"\x00")
        gen_hash = sha1(gen_bytes)
        xor_hash = b""
        for m_byte, g_byte in zip(modulus_hash, gen_hash):
            xor_hash += int.to_bytes(m_byte^g_byte, 1, "little")

        client_eph = int.to_bytes(client_ephemeral, 32, "little")
        server_eph = int.to_bytes(self.server_ephemeral, 32, "little")

        to_hash = ( xor_hash + sha1(account.name.encode("ascii")) +
                    account.srp_salt_as_bytes +
                    client_eph + server_eph + self.session_key )
        self.client_proof = sha1(to_hash)

    def generate_server_proof(self, client_ephemeral):
        assert self.session_key
        assert self.client_proof
        client_eph = int.to_bytes(client_ephemeral, 32, "little")
        to_hash = client_eph + self.client_proof + self.session_key
        self.server_proof = sha1(to_hash)

    @staticmethod
    def generate_account_srp_data(account, password):
        """ Generate a salt and a verifier for that account and that pass. """
        ident = account.name.upper()
        password = password.upper()
        salt = os.urandom(32)
        verifier = Srp._generate_verifier(ident, password, salt)
        account.srp_salt_as_bytes = salt
        account.srp_verifier_as_int = verifier

    @staticmethod
    def _generate_verifier(ident, password, salt):
        """ Generate an SRP verifier from these log informations. """
        logs = ident + ":" + password
        logs_hash = sha1(logs.encode("ascii"))
        x_content = salt + logs_hash
        x_bytes = sha1(x_content)
        x_int = int.from_bytes(x_bytes, "little")
        verifier = pow(Srp.GENERATOR, x_int, Srp.MODULUS)
        return verifier
