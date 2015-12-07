import time
import threading

from durator.auth.constants import LoginOpCodes
from durator.auth.login_challenge import LoginChallenge
from durator.auth.login_connection_state import LoginConnectionState
from durator.auth.login_proof import LoginProof
from durator.auth.srp import Srp
from durator.utils.logger import LOG
from durator.utils.misc import dump_data


class LoginConnection(object):
    """ Handle the login process of a client with a SRP challenge. """

    LEGAL_OPS = {
        LoginConnectionState.INIT:        [LoginOpCodes.LOGIN_CHALL],
        LoginConnectionState.CLOSED:      [],
        LoginConnectionState.SENT_CHALL:  [LoginOpCodes.LOGIN_PROOF]
    }

    OP_HANDLERS = {
        LoginOpCodes.LOGIN_CHALL: LoginChallenge,
        LoginOpCodes.LOGIN_PROOF: LoginProof
    }

    def __init__(self, server, connection, address):
        self.server = server
        self.socket = connection
        self.address = address
        self.state = LoginConnectionState.INIT
        self.pass_entry = None
        self.srp = Srp()

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

    def threaded_handle_connection(self):
        """ Start another thread to handle the connection. """
        connection_thread = threading.Thread(target = self.handle_connection)
        connection_thread.daemon = True
        connection_thread.start()

    def handle_connection(self):
        while self.state != LoginConnectionState.CLOSED:
            data = self.socket.recv(1024)
            if not data:
                LOG.debug("Client closed the connection.")
                break
            self._handle_packet(data)

    def _handle_packet(self, data):
        print("<<<")
        print(dump_data(data), end = "")

        opcode, packet = LoginOpCodes(data[0]), data[1:]
        if not self.is_opcode_legal(opcode):
            LOG.debug( "Received illegal opcode " + str(opcode)
                     + " in state " + str(self.state) )
            self.close_connection()
            return

        handler_class = LoginConnection.OP_HANDLERS.get(opcode)
        if handler_class is None:
            LOG.debug("Unknown operation: " + str(opcode))
            self.close_connection()
            return

        self._call_handler(handler_class, packet)

    def _call_handler(self, handler_class, packet):
        handler = handler_class(self, packet)
        next_state, response = handler.process()

        if response:
            print(">>>")
            print(dump_data(response), end = "")
            time.sleep(0.1)
            self.socket.sendall(response)

        self.state = next_state
        if self.state == LoginConnectionState.CLOSED:
            self.close_connection()
