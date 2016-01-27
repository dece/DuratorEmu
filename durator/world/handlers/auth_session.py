from enum import Enum
import io
from struct import Struct

from durator.common.account.managers import AccountSessionManager
from durator.common.crypto.session_cipher import SessionCipher
from durator.common.crypto.sha1 import sha1
from durator.config import CONFIG
from durator.world.world_connection_state import WorldConnectionState
from durator.world.opcodes import OpCode
from durator.world.world_packet import WorldPacket
from pyshgck.bin import read_cstring, read_struct
from pyshgck.logger import LOG


class AuthSessionResponseCode(Enum):

    AUTH_OK                     = 0x0C
    AUTH_FAILED                 = 0x0D
    AUTH_REJECT                 = 0x0E
    AUTH_BAD_SERVER_PROOF       = 0x0F
    AUTH_UNAVAILABLE            = 0x10
    AUTH_SYSTEM_ERROR           = 0x11
    AUTH_BILLING_ERROR          = 0x12
    AUTH_BILLING_EXPIRED        = 0x13
    AUTH_VERSION_MISMATCH       = 0x14
    AUTH_UNKNOWN_ACCOUNT        = 0x15
    AUTH_INCORRECT_PASSWORD     = 0x16
    AUTH_SESSION_EXPIRED        = 0x17
    AUTH_SERVER_SHUTTING_DOWN   = 0x18
    AUTH_ALREADY_LOGGING_IN     = 0x19
    AUTH_LOGIN_SERVER_NOT_FOUND = 0x1A
    AUTH_WAIT_QUEUE             = 0x1B
    AUTH_BANNED                 = 0x1C
    AUTH_ALREADY_ONLINE         = 0x1D
    AUTH_NO_TIME                = 0x1E
    AUTH_DB_BUSY                = 0x1F
    AUTH_SUSPENDED              = 0x20
    AUTH_PARENTAL_CONTROL       = 0x21


class AuthSessionHandler(object):
    """ Handle the session request sent by the client and initialise the session
    cipher in the process. """

    PACKET_PART1_BIN  = Struct("<2I")
    PACKET_PART2_BIN  = Struct("<I20s")
    RESPONSE_SUCC_BIN = Struct("<BIBI")
    RESPONSE_FAIL_BIN = Struct("<B")

    def __init__(self, connection, packet):
        self.conn = connection
        self.packet = packet

        self.build = 0
        self.unk = 0
        self.account_name = ""
        self.client_seed = 0
        self.client_hash = b""

        self.session_key = b""
        self.server_hash = b""

    def process(self):
        self._parse_packet(self.packet)

        # We start by loading the session key because in any case the client
        # expects an encrypted response.
        self._load_session_key()
        if not self.session_key:
            LOG.warning("A client not logged in tried to join world server.")
            return self.conn.MAIN_ERROR_STATE, None

        self._setup_encryption()

        if self.build != int(CONFIG["general"]["build"]):
            LOG.warning("Wrong build tried to auth to world server: {}".format(
                str(self.build)
            ))
            error_code = AuthSessionResponseCode.AUTH_VERSION_MISMATCH
            response = self._get_failure_packet(error_code)
            return self.conn.MAIN_ERROR_STATE, response

        self._generate_server_hash()
        if self.server_hash != self.client_hash:
            LOG.warning("Wrong client hash in world server auth.")
            error_code = AuthSessionResponseCode.AUTH_REJECT
            response = self._get_failure_packet(error_code)
            return self.conn.MAIN_ERROR_STATE, response

        # Once the session cipher is up and the client is fully checked,
        # accept the authentication and move on.
        LOG.debug("World server auth OK.")
        response = self._get_success_packet()
        return WorldConnectionState.AUTH_OK, response

    def _parse_packet(self, packet):
        packet_io = io.BytesIO(packet)
        part1_data = read_struct(packet_io, self.PACKET_PART1_BIN)
        self.build = part1_data[0]
        self.unk = part1_data[1]

        account_name_bytes = read_cstring(packet_io, packet_io.tell())
        self.account_name = account_name_bytes.decode("ascii")

        part2_data = read_struct(packet_io, self.PACKET_PART2_BIN)
        self.client_seed = part2_data[0]
        self.client_hash = part2_data[1]

    def _load_session_key(self):
        session = AccountSessionManager.get_session(self.account_name)
        if session is not None:
            self.conn.account = session.account
            self.session_key = session.session_key_as_bytes

    def _generate_server_hash(self):
        auth_seed = self.conn.shared_data["auth_seed"]
        del self.conn.shared_data["auth_seed"]
        to_hash = ( self.account_name.encode("ascii") +
                    bytes(4) +
                    int.to_bytes(self.client_seed, 4, "little") +
                    int.to_bytes(auth_seed, 4, "little") +
                    self.session_key )
        self.server_hash = sha1(to_hash)

    def _setup_encryption(self):
        """ Set up the session cipher and return True on success. """
        self.conn.set_session_cipher(SessionCipher(self.session_key))

    def _get_success_packet(self):
        data = self.RESPONSE_SUCC_BIN.pack(
            AuthSessionResponseCode.AUTH_OK.value,
            0,  # BillingTimeRemaining
            0,  # BillingPlanFlags
            0   # BillingTimeRested
        )
        return WorldPacket(OpCode.SMSG_AUTH_RESPONSE, data)

    def _get_failure_packet(self, error_code):
        data = self.RESPONSE_FAIL_BIN.pack(error_code.value)
        return WorldPacket(OpCode.SMSG_AUTH_RESPONSE, data)
