import os
from struct import Struct

from durator.auth.constants import LoginOpCode, LoginResult
from durator.auth.login_connection_state import LoginConnectionState
from durator.auth.srp import Srp
from durator.common.account.account import AccountStatus
from durator.common.account.managers import AccountManager
from pyshgck.logger import LOG


class LoginChallenge(object):
    """ Process a challenge request and answer with the challenge data. """

    HEADER_BIN        = Struct("<BH")
    CONTENT_BIN       = Struct("<4s3BH4s4s4sI4BB")
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

        self.game_name = _decode_chall_cstring(content_data[0])
        self.version_major = content_data[1]
        self.version_minor = content_data[2]
        self.version_patch = content_data[3]
        self.version_build = content_data[4]
        self.arch = _decode_chall_cstring(content_data[5])
        self.platform = _decode_chall_cstring(content_data[6])
        self.locale = _decode_chall_cstring(content_data[7])
        self.timezone = content_data[8]
        self.ip_address = content_data[9:13]
        self.account_name_size = content_data[13]

        account_name = packet[ end_offset : end_offset+self.account_name_size ]
        self.account_name = account_name.decode("ascii")

    def _process_account(self):
        """ Check if the account received can log to the server. """
        account = AccountManager.get_account(self.account_name)
        if account is not None and account.is_valid():
            self.conn.account = account
            self.conn.srp.generate_server_ephemeral(account.srp_verifier_as_int)
            response = self._get_success_response()
            return LoginConnectionState.SENT_CHALL, response
        else:
            LOG.warning("Invalid account {} tried to login".format(
                self.account_name
            ))
            response = self._get_failure_response(account)
            return LoginConnectionState.CLOSED, response

    def _get_success_response(self):
        """ Return a success packet with appropriate SRP data. """
        server_eph = int.to_bytes(self.conn.srp.server_ephemeral, 32, "little")
        salt = self.conn.account.srp_salt_as_bytes
        generator = int.to_bytes(Srp.GENERATOR, 1, "little")
        modulus = int.to_bytes(Srp.MODULUS, 32, "little")

        response = self.RESPONSE_SUCC_BIN.pack(
            LoginOpCode.LOGIN_CHALL.value,
            0,
            LoginResult.SUCCESS.value,
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
        AccountStatus.SUSPENDED: LoginResult.FAIL_SUSPENDED,
        AccountStatus.BANNED:    LoginResult.FAIL_BANNED
    }

    def _get_failure_response(self, account):
        """ Return a failure packet with appropriate error code. """
        if account is None:
            fail_code = LoginResult.FAIL_1
        else:
            account_status = AccountStatus(account.status)
            fail_code = ( self.ERROR_CODES.get(account_status)
                          or LoginResult.FAIL_1 )
        response = self.RESPONSE_FAIL_BIN.pack(
            LoginOpCode.LOGIN_CHALL.value,
            0,
            fail_code.value
        )
        return response


def _decode_chall_cstring(cstring, encoding = "ascii"):
    return cstring.decode(encoding).strip("\x00")[::-1]
