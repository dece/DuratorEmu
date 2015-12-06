import socket

from durator.auth.account import Account
from durator.auth.login_connection import LoginConnection
from durator.auth.srp import Srp


class LoginServer(object):
    """ Listen for clients and start a new thread for each connection. """

    HOST = "0.0.0.0"
    PORT = 3724
    BACKLOG_SIZE = 64

    def __init__(self):
        self.socket = None

    def start(self):
        self._start_listening()
        self._accept_connections()
        self._stop_listening()

    def _start_listening(self):
        """ Start listening with a non-blocking socket,
        to still capture Windows signals. """
        self.socket = socket.socket()
        self.socket.settimeout(1)
        self.socket.bind( (LoginServer.HOST, LoginServer.PORT) )
        self.socket.listen(LoginServer.BACKLOG_SIZE)
        print("Login server running.")

    def _accept_connections(self):
        try:
            while True:
                self._try_accept_connection()
        except KeyboardInterrupt:
            print("KeyboardInterrupt received, stopping server.")

    def _try_accept_connection(self):
        try:
            connection, address = self.socket.accept()
            self._handle_connection(connection, address)
        except socket.timeout:
            pass

    def _handle_connection(self, connection, address):
        print("Accepting connection from", address)
        login_connection = LoginConnection(self, connection, address)
        login_connection.threaded_handle_connection()

    def _stop_listening(self):
        self.socket.close()
        self.socket = None
        print("Login server stopped.")

    def get_account(self, account_name):
        """ (TEMP) Create a dummy account with account name as password. """
        return Account.get_dummy_account(account_name)
