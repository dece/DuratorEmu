import os
from struct import Struct

from durator.auth.constants import LoginOpCodes, LoginResults
from durator.auth.login_connection_state import LoginConnectionState
from pyshgck.logger import LOG


class ReconChallenge(object):

    HEADER_BIN = Struct("<BH")
    CONTENT_BIN = Struct("<4s3BH4s4s4sI4BB")
    RESPONSE_SUCC_BIN = Struct("<2B16s2Q")
    RESPONSE_FAIL_BIN = Struct("<2B")

    def __init__(self, connection, packet):
        self.conn = connection
        self.packet = packet

        self.unk_code = 0
        self.size = 0
        self.account_name_size = 0
        self.account_name = ""

    def process(self):
        self._parse_packet(self.packet)
        return self._process_reconnection()

    def _parse_packet(self, packet):
        self._parse_packet_header(packet)
        self._parse_packet_content(packet)

    def _parse_packet_header(self, packet):
        end_offset = ReconChallenge.HEADER_BIN.size
        header = packet[ 0 : end_offset ]
        header_data = ReconChallenge.HEADER_BIN.unpack(header)
        self.unk_code = header_data[0]
        self.size = header_data[1]

    def _parse_packet_content(self, packet):
        offset = ReconChallenge.HEADER_BIN.size
        end_offset = offset + ReconChallenge.CONTENT_BIN.size
        content = packet[ offset : end_offset ]
        content_data = ReconChallenge.CONTENT_BIN.unpack(content)

        self.account_name_size = content_data[13]

        account_name = packet[ end_offset : end_offset+self.account_name_size ]
        self.account_name = account_name.decode("ascii")

    def _process_reconnection(self):
        session = self.conn.server.get_account_session(self.account_name)
        if session is not None:
            LOG.debug("Reconnection: account was logged in.")
            self.conn.account = session.account
            self.conn.recon_challenge = os.urandom(16)
            response = self._get_success_response()
            return LoginConnectionState.RECON_CHALL, response
        else:
            LOG.warning("Reconnection: Account wasn't logged in!")
            response = self._get_failure_response()
            return LoginConnectionState.CLOSED, response

    def _get_success_response(self):
        response = ReconChallenge.RESPONSE_SUCC_BIN.pack(
            LoginOpCodes.RECON_CHALL.value,
            LoginResults.SUCCESS.value,
            self.conn.recon_challenge,
            0,
            0
        )
        return response

    def _get_failure_response(self):
        response = ReconChallenge.RESPONSE_FAIL_BIN.pack(
            LoginOpCodes.RECON_CHALL.value,
            LoginResults.FAIL_1.value
        )
        return response
