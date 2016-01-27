import os
from struct import Struct

from durator.auth.constants import LoginOpCode, LoginResult
from durator.auth.login_connection_state import LoginConnectionState
from durator.common.account.managers import AccountSessionManager
from durator.db.database import db_connection
from pyshgck.logger import LOG


class ReconChallenge(object):
    """ Handle a client's reconnection challenge request (opcode 0x2). """

    HEADER_BIN        = Struct("<BH")
    CONTENT_BIN       = Struct("<4s3BH4s4s4sI4BB")
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
        end_offset = self.HEADER_BIN.size
        header = packet[ 0 : end_offset ]
        header_data = self.HEADER_BIN.unpack(header)
        self.unk_code = header_data[0]
        self.size = header_data[1]

    def _parse_packet_content(self, packet):
        offset = self.HEADER_BIN.size
        end_offset = offset + self.CONTENT_BIN.size
        content = packet[ offset : end_offset ]
        content_data = self.CONTENT_BIN.unpack(content)

        self.account_name_size = content_data[13]

        account_name = packet[ end_offset : end_offset+self.account_name_size ]
        self.account_name = account_name.decode("ascii")

    def _process_reconnection(self):
        session = AccountSessionManager.get_session(self.account_name)
        if session is not None:
            LOG.debug("Reconnection: account was logged in.")
            self.conn.account = ReconChallenge._get_session_account(session)
            self.conn.recon_challenge = os.urandom(16)
            response = self._get_success_response()
            return LoginConnectionState.RECON_CHALL, response
        else:
            LOG.warning("Reconnection: account wasn't logged in!")
            response = self._get_failure_response()
            return LoginConnectionState.CLOSED, response

    @staticmethod
    @db_connection
    def _get_session_account(session):
        return session.account

    def _get_success_response(self):
        response = self.RESPONSE_SUCC_BIN.pack(
            LoginOpCode.RECON_CHALL.value,
            LoginResult.SUCCESS.value,
            self.conn.recon_challenge,
            0,
            0
        )
        return response

    def _get_failure_response(self):
        response = self.RESPONSE_FAIL_BIN.pack(
            LoginOpCode.RECON_CHALL.value,
            LoginResult.FAIL_1.value
        )
        return response
