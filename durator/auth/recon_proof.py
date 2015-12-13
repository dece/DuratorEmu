from struct import Struct

from durator.auth.constants import LoginOpCode, LoginResult
from durator.auth.login_connection_state import LoginConnectionState
from durator.common.crypto import sha1
from pyshgck.logger import LOG


class ReconProof(object):
    """ Handle a client's reconnection proof request (opcode 0x3). """

    CONTENT_BIN       = Struct("<16s20s20sB")
    RESPONSE_SUCC_BIN = Struct("<2B")
    RESPONSE_FAIL_BIN = Struct("<2B")

    def __init__(self, connection, packet):
        self.conn = connection
        self.packet = packet

        self.proof_data = b""
        self.client_proof = b""
        self.unk_data = b""
        self.unk = 0

        self.local_proof = b""

    def process(self):
        self._parse_packet(self.packet)
        self._generate_local_proof()
        if self.client_proof == self.local_proof:
            LOG.debug("Reconnection: correct proof")
            response = self._get_success_response()
            return LoginConnectionState.RECON_PROOF, response
        else:
            LOG.warning("Reconnection: wrong proof!")
            response = self._get_failure_response()
            return LoginConnectionState.CLOSED, response

    def _parse_packet(self, packet):
        data = ReconProof.CONTENT_BIN.unpack(packet)
        self.proof_data = data[0]
        self.client_proof = data[1]
        self.unk_data = data[2]
        self.unk = data[3]

    def _generate_local_proof(self):
        account_name = self.conn.account.name
        session = self.conn.server.get_account_session(account_name)
        challenge = self.conn.recon_challenge
        to_hash = ( account_name.encode("ascii") + self.proof_data +
                    challenge + session.session_key_as_bytes )
        self.local_proof = sha1(to_hash)

    def _get_success_response(self):
        response = ReconProof.RESPONSE_SUCC_BIN.pack(
            LoginOpCode.RECON_PROOF.value,
            LoginResult.SUCCESS.value
        )
        return response

    def _get_failure_response(self):
        response = ReconProof.RESPONSE_FAIL_BIN.pack(
            LoginOpCode.RECON_PROOF.value,
            LoginResult.FAIL_1.value
        )
        return response
