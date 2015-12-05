""" Clunky implementation of the SRP login process """

import hashlib
import os
import random

from durator.utils import hexlify

random.seed()


class Srp(object):
    """ SRP login manager

    Attributes:
        priv_ephemeral: big private integer (b)
        server_ephemeral: big private integer (B)
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
        self._gen_priv_ephemeral()
        self.server_ephemeral = 0
        self.session_key = b""
        self.client_proof = b""
        self.server_proof = b""

    def _gen_priv_ephemeral(self):
        """ Generate the private ephemeral (b) """
        random_19_bytes = os.urandom(19)
        big_random_int = int.from_bytes(random_19_bytes, "little")
        priv_ephemeral = big_random_int % Srp.MODULUS
        self.priv_ephemeral = priv_ephemeral

    def gen_server_ephemeral(self, verifier):
        """ Generate the server ephemeral (B) """
        big_integer = pow(Srp.GENERATOR, self.priv_ephemeral, Srp.MODULUS)
        ephemeral = (Srp.MULTIPLIER * verifier + big_integer) % Srp.MODULUS
        self.server_ephemeral = ephemeral

    def verify_proof(self, proof, pass_entry):
        """ Generate a session key, then the client proof and check it with
        the received proof. Return True if the proof is OK, and so is the
        session key. """
        self._gen_session_key(proof.client_ephemeral, pass_entry.verifier)
        self._gen_client_proof(proof, pass_entry)
        return proof.client_proof == self.client_proof

    def _gen_session_key(self, client_eph, verifier):
        scramble = Srp._scramble_a_b(client_eph, self.server_ephemeral)
        pow_verifier = pow(verifier, scramble, Srp.MODULUS)
        pow_verifier *= client_eph
        to_interleave = pow(pow_verifier, self.priv_ephemeral, Srp.MODULUS)
        self.session_key = _sha1_interleave(to_interleave)
        print("Session key: " + hexlify(self.session_key))

    @staticmethod
    def _scramble_a_b(big_int_a, big_int_b):
        a_bytes = int.to_bytes(big_int_a, 32, "little")
        b_bytes = int.to_bytes(big_int_b, 32, "little")
        scramble_hash = _sha1(a_bytes + b_bytes)
        scramble = int.from_bytes(scramble_hash, "little")
        return scramble

    def _gen_client_proof(self, proof, pass_entry):
        modulus_bytes = int.to_bytes(Srp.MODULUS, 32, "little").rstrip(b"\x00")
        modulus_hash = _sha1(modulus_bytes)
        gen_bytes = int.to_bytes(Srp.GENERATOR, 32, "little").rstrip(b"\x00")
        gen_hash = _sha1(gen_bytes)
        xor_hash = b""
        for m_byte, g_byte in zip(modulus_hash, gen_hash):
            xor_hash += int.to_bytes(m_byte^g_byte, 1, "little")

        client_eph = int.to_bytes(proof.client_ephemeral, 32, "little")
        server_eph = int.to_bytes(self.server_ephemeral, 32, "little")

        to_hash = ( xor_hash + _sha1(pass_entry.ident.encode("ascii")) +
                    pass_entry.salt + client_eph + server_eph +
                    self.session_key )
        self.client_proof = _sha1(to_hash)
        print("Generated client proof: " + hexlify(self.client_proof))

    def gen_server_proof(self, proof):
        client_eph = int.to_bytes(proof.client_ephemeral, 32, "little")
        to_hash = client_eph + self.client_proof + self.session_key
        self.server_proof = _sha1(to_hash)

    @staticmethod
    def gen_pass_entry(ident, password):
        ident = ident.upper()
        password = password.upper()
        salt = os.urandom(32)
        verifier = Srp._gen_verifier(ident, password, salt)
        pass_entry = SrpPassEntry(ident, verifier, salt)
        return pass_entry

    @staticmethod
    def _gen_verifier(ident, password, salt):
        logs = ident + ":" + password
        logs_hash = _sha1(logs.encode("ascii"))
        x_content = salt + logs_hash
        x_bytes = _sha1(x_content)
        x_int = int.from_bytes(x_bytes, "little")
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

def _sha1_interleave(big_int):
    big_array = int.to_bytes(big_int, 128, "little")
    big_array = big_array.rstrip(b"\x00")
    if len(big_array) % 2 == 1:
        big_array = big_array[1:]

    part1 = b""
    part2 = b""
    for i in range(len(big_array)):
        if i % 2 == 0:
            part1 += big_array[i:i+1]
        else:
            part2 += big_array[i:i+1]

    hash1 = _sha1(part1)
    hash2 = _sha1(part2)
    interleaved = b""
    for i in range(20):
        interleaved += hash1[i:i+1] + hash2[i:i+1]

    return interleaved
