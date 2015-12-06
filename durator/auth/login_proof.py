from struct import Struct

from durator.auth.constants import LoginOpCodes, LoginResults
from durator.auth.login_connection_state import LoginConnectionState
from durator.utils.misc import hexlify


class LoginProof(object):
    """ Process a proof request and answer with the server proof. """

    PROOF_BIN = Struct("<32s20s20sB")
    RESPONSE_SUCC_BIN = Struct("<2B20sI")
    RESPONSE_FAIL_BIN = Struct("<2B")

    def __init__(self, connection, packet):
        self.conn = connection
        self.packet = packet

        self.client_ephemeral = 0
        self.client_proof = b""
        self.checksum = b""
        self.unk = 0

    def process(self):
        self._parse_packet(self.packet)
        print("Received proof: " + hexlify(self.client_proof))

        account = self.conn.account
        verifier = account.srp_verifier
        self.conn.srp.generate_session_key(self.client_ephemeral, verifier)
        self.conn.srp.generate_client_proof(self.client_ephemeral, account)
        local_client_proof = self.conn.srp.client_proof

        if local_client_proof == self.client_proof:
            print("Authenticated!")
            self.conn.srp.generate_server_proof(self.client_ephemeral)
            response = self._get_success_response()
            return LoginConnectionState.SENT_PROOF, response
        else:
            print("WRONG PROOF!")
            response = self._get_failure_response()
            return LoginConnectionState.CLOSED, response

    def _parse_packet(self, packet):
        data = LoginProof.PROOF_BIN.unpack(packet)
        self.client_ephemeral = int.from_bytes(data[0], "little")
        self.client_proof = data[1]
        self.checksum = data[2]
        self.unk = data[3]

    def _get_success_response(self):
        response = LoginProof.RESPONSE_SUCC_BIN.pack(
            LoginOpCodes.LOGIN_PROOF.value,
            LoginResults.SUCCESS.value,
            self.conn.srp.server_proof,
            0
        )
        return response

    def _get_failure_response(self):
        response = LoginProof.RESPONSE_FAIL_BIN.pack(
            LoginOpCodes.LOGIN_PROOF.value,
            LoginResults.FAIL_1.value
        )
        return response
