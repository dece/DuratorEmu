import socket
import threading

from durator.auth.account import Account
from durator.auth.login_connection import LoginConnection
from pyshgck.concurrency import simple_thread
from pyshgck.logger import LOG


def access_logged_in_list(func):
    def decorator(self, *args, **kwargs):
        self.logged_in_lock.acquire()
        return_value = func(self, *args, **kwargs)
        self.logged_in_lock.release()
        return return_value
    return decorator


class LoginServer(object):
    """ Listen for clients and start a new thread for each connection. """

    HOST = "0.0.0.0"
    PORT = 3724
    BACKLOG_SIZE = 64

    def __init__(self):
        self.socket = None
        self.logged_in = {}
        self.logged_in_lock = threading.Lock()

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
        LOG.info("Login server running.")

    def _accept_connections(self):
        try:
            while True:
                self._try_accept_connection()
        except KeyboardInterrupt:
            LOG.info("KeyboardInterrupt received, stopping server.")

    def _try_accept_connection(self):
        try:
            connection, address = self.socket.accept()
            self._handle_connection(connection, address)
        except socket.timeout:
            pass

    def _handle_connection(self, connection, address):
        LOG.info("Accepting connection from " + str(address))
        login_connection = LoginConnection(self, connection, address)
        simple_thread(login_connection.handle_connection)

    def _stop_listening(self):
        self.socket.close()
        self.socket = None
        LOG.info("Login server stopped.")

    def get_account(self, account_name):
        """ (TEMP) Create a dummy account with account name as password. """
        return Account.get_dummy_account(account_name)

    @access_logged_in_list
    def accept_account_login(self, account, session_key):
        self.logged_in[account.name] = {
            "account": account,
            "session_key": session_key
        }

    @access_logged_in_list
    def logout_account(self, account):
        del self.logged_in[account.name]

    @access_logged_in_list
    def is_logged_in(self, account_name):
        is_logged_in = account_name in self.logged_in
        return is_logged_in

    @access_logged_in_list
    def get_logged_in_account(self, account_name):
        return self.logged_in[account_name]["account"]

    @access_logged_in_list
    def get_logged_in_session_key(self, account_name):
        return self.logged_in[account_name]["session_key"]
