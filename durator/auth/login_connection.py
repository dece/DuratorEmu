from durator.auth.constants import LoginOpCode
from durator.auth.login_challenge import LoginChallenge
from durator.auth.login_connection_state import LoginConnectionState
from durator.auth.login_proof import LoginProof
from durator.auth.realmlist_request import RealmlistRequest
from durator.auth.recon_challenge import ReconChallenge
from durator.auth.recon_proof import ReconProof
from durator.auth.srp import Srp
from pyshgck.logger import LOG


class LoginConnection(object):
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

    def __init__(self, server, connection, address):
        self.server = server
        self.socket = connection
        self.address = address
        self.state = LoginConnectionState.INIT
        self.account = None
        self.srp = Srp()
        self.recon_challenge = b""

    def __del__(self):
        self.socket.close()

    def is_opcode_legal(self, opcode):
        """ Check if that opcode is legal for the current connection state. """
        return opcode in LoginConnection.LEGAL_OPS[self.state]

    def close_connection(self):
        """ Close connection with client. """
        self.state = LoginConnectionState.CLOSED
        self.socket.close()
        LOG.debug("Server closed the connection.")

    def handle_connection(self):
        while self.state != LoginConnectionState.CLOSED:
            data = self.socket.recv(1024)
            if not data:
                LOG.debug("Client closed the connection.")
                break
            self._try_handle_packet(data)

    def _try_handle_packet(self, data):
        try:
            self._handle_packet(data)
        except Exception:
            LOG.error("Uncaught exception in LoginConnection._handle_packet")
            raise

    def _handle_packet(self, data):
        """ Handle packet and update connection state.

        If the packet has a legal opcode for that state, the appropriate handler
        class is grabbed and instantiated.
        """
        opcode, packet = LoginOpCodes(data[0]), data[1:]
        if not self.is_opcode_legal(opcode):
            LOG.warning( "Connection: received illegal opcode " + str(opcode)
                       + " in state " + str(self.state) )
            self.close_connection()
            return

        handler_class = LoginConnection.OP_HANDLERS.get(opcode)
        if handler_class is None:
            LOG.warning("Connection: unknown operation: " + str(opcode))
            self.close_connection()
            return

        self._call_handler(handler_class, packet)

    def _call_handler(self, handler_class, packet):
        """ Instantiate a handle with that packet and process its result.

        The handler returns the next state of the connection (or None if state
        should stay the same) and bytes that should be sent back to the client
        (if not empty).
        """
        handler = handler_class(self, packet)
        next_state, response = handler.process()

        if response:
            self.socket.sendall(response)

        if next_state is not None:
            self.state = next_state
        if self.state == LoginConnectionState.CLOSED:
            self.close_connection()

    def accept_login(self):
        session_key = self.srp.session_key
        self.server.accept_account_login(self.account, session_key)
