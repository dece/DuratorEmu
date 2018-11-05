from durator.auth.constants import LoginOpCode
from durator.auth.login_challenge import LoginChallenge
from durator.auth.login_connection_state import LoginConnectionState
from durator.auth.login_proof import LoginProof
from durator.auth.realmlist_request import RealmlistRequest
from durator.auth.recon_challenge import ReconChallenge
from durator.auth.recon_proof import ReconProof
from durator.auth.srp import Srp
from durator.common.networking.connection_automaton import ConnectionAutomaton
from durator.common.log import LOG
from durator.config import DEBUG
from pyshgck.format import get_data_dump


class LoginConnection(ConnectionAutomaton):
    """ Handle the login process of a client with a SRP challenge. """

    LEGAL_OPS = {
        LoginConnectionState.INIT:        [ LoginOpCode.LOGIN_CHALL
                                          , LoginOpCode.RECON_CHALL ],
        LoginConnectionState.CLOSED:      [ ],
        LoginConnectionState.SENT_CHALL:  [ LoginOpCode.LOGIN_PROOF ],
        LoginConnectionState.SENT_PROOF:  [ LoginOpCode.REALMLIST ],
        LoginConnectionState.RECON_CHALL: [ LoginOpCode.RECON_PROOF ],
        LoginConnectionState.RECON_PROOF: [ LoginOpCode.REALMLIST ],
    }

    OP_HANDLERS = {
        LoginOpCode.LOGIN_CHALL: LoginChallenge,
        LoginOpCode.LOGIN_PROOF: LoginProof,
        LoginOpCode.RECON_CHALL: ReconChallenge,
        LoginOpCode.RECON_PROOF: ReconProof,
        LoginOpCode.REALMLIST:   RealmlistRequest
    }

    INIT_STATE       = LoginConnectionState.INIT
    END_STATES       = [ LoginConnectionState.CLOSED ]
    MAIN_ERROR_STATE = LoginConnectionState.CLOSED

    def __init__(self, server, connection):
        super().__init__(connection)
        self.server = server
        self.account = None
        self.srp = Srp()
        self.recon_challenge = b""

    def __del__(self):
        self.socket.close()

    def _recv_packet(self):
        # This assumes that all packets are received in no more or less than one
        # piece, which is a wrong. However, exceptions shouldn't occur often
        # with how short login messages are.
        try:
            data = self.socket.recv(1024)
            if data and DEBUG:
                print(get_data_dump(data), end = "")
            return data or None
        except ConnectionError:
            LOG.info("Lost connection.")
            return None

    def _parse_packet(self, packet):
        return LoginOpCode(packet[0]), packet[1:]

    def send_packet(self, packet):
        self.socket.sendall(packet)

    def _actions_after_main_loop(self):
        """ Close connection with client. """
        LOG.debug("LoginConnection: session ended.")
        self.socket.close()

    def accept_login(self):
        """ Ask the login server to validate this account session. """
        self.server.accept_account_login(self.account, self.srp.session_key)
