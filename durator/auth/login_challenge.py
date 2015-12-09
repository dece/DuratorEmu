import os
from struct import Struct

from durator.auth.account import Account
from durator.auth.constants import LoginOpCodes, LoginResults
from durator.auth.login_connection_state import LoginConnectionState
from durator.auth.srp import Srp
from durator.utils.network_formats import netstr_to_str
from pyshgck.logger import LOG


class LoginChallenge(object):
    """ Process a challenge request and answer with the challenge data. """

    HEADER_BIN = Struct("<BH")
    CONTENT_BIN = Struct("<4s3BH4s4s4sI4BB")
    RESPONSE_SUCC_BIN = Struct("<3B32sB1sB32s32s16s")
    RESPONSE_FAIL_BIN = Struct("<3B")

    def __init__(self, connection, packet):
        self.conn = connection
        self.packet = packet

        self.unk_code = 0
        self.size = 0
        self.game_name = ""
        self.version_major = 0
        self.version_minor = 0
        self.version_patch = 0
        self.version_build = 0
        self.arch = ""
        self.platform = ""
        self.locale = ""
        self.timezone = 0
        self.ip_address = (0, 0, 0, 0)
        self.account_name_size = 0
        self.account_name = ""

    def process(self):
        """ Process the challenge packet: parse its data and check whether that
        account name can log. """
        self._parse_packet(self.packet)
        LOG.debug("Login: account " + self.account_name)
        return self._process_account()

    def _parse_packet(self, packet):
        self._parse_packet_header(packet)
        self._parse_packet_content(packet)

    def _parse_packet_header(self, packet):
        end_offset = LoginChallenge.HEADER_BIN.size
        header = packet[ 0 : end_offset ]
        header_data = LoginChallenge.HEADER_BIN.unpack(header)
        self.unk_code = header_data[0]
        self.size = header_data[1]

    def _parse_packet_content(self, packet):
        offset = LoginChallenge.HEADER_BIN.size
        end_offset = offset + LoginChallenge.CONTENT_BIN.size
        content = packet[ offset : end_offset ]
        content_data = LoginChallenge.CONTENT_BIN.unpack(content)

        self.game_name = netstr_to_str(content_data[0])
        self.version_major = content_data[1]
        self.version_minor = content_data[2]
        self.version_patch = content_data[3]
        self.version_build = content_data[4]
        self.arch = netstr_to_str(content_data[5])
        self.platform = netstr_to_str(content_data[6])
        self.locale = netstr_to_str(content_data[7])
        self.timezone = content_data[8]
        self.ip_address = content_data[9:13]
        self.account_name_size = content_data[13]

        account_name = packet[ end_offset : end_offset+self.account_name_size ]
        self.account_name = account_name.decode("ascii")

    def _process_account(self):
        """ Check if the account received can log to the server. TODO checks """
        account = self.conn.server.get_account(self.account_name)
        if account.can_log():
            self.conn.account = account
            self.conn.srp.generate_server_ephemeral(account.srp_verifier)
            response = self._get_success_response()
            return LoginConnectionState.SENT_CHALL, response
        else:
            response = self._get_failure_response(account)
            return LoginConnectionState.CLOSED, response

    def _get_success_response(self):
        """ Return a success packet with appropriate SRP data. """
        server_eph = int.to_bytes(self.conn.srp.server_ephemeral, 32, "little")
        salt = self.conn.account.srp_salt
        generator = int.to_bytes(Srp.GENERATOR, 1, "little")
        modulus = int.to_bytes(Srp.MODULUS, 32, "little")

        response = LoginChallenge.RESPONSE_SUCC_BIN.pack(
            LoginOpCodes.LOGIN_CHALL.value,
            0,
            LoginResults.SUCCESS.value,
            server_eph,
            len(generator),
            generator,
            len(modulus),
            modulus,
            salt,
            os.urandom(16)
        )
        return response

    ERROR_CODES = {
        Account.Status.SUSPENDED: LoginResults.FAIL_SUSPENDED,
        Account.Status.BANNED:    LoginResults.FAIL_BANNED
    }

    def _get_failure_response(self, account):
        """ Return a failure packet with appropriate error code. """
        fail_code = LoginChallenge.ERROR_CODES.get(account.status)
        if fail_code is None:
            fail_code = LoginResults.FAIL_1
        response = LoginChallenge.RESPONSE_FAIL_BIN.pack(
            LoginOpCodes.LOGIN_CHALL.value,
            0,
            fail_code.value
        )
        return response
