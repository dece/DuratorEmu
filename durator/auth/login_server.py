import socket
import threading
import time

from durator.auth.account import AccountManager
from durator.auth.login_connection import LoginConnection
from durator.auth.realm_connection import RealmConnection
from pyshgck.concurrency import simple_thread
from pyshgck.logger import LOG


def access_logged_in_list(func):
    def decorator(self, *args, **kwargs):
        with self.logged_in_lock:
            return_value = func(self, *args, **kwargs)
        return return_value
    return decorator


class LoginServer(object):
    """ Listen for clients and start a new thread for each connection.

    The LoginServer listens for clients (main socket) but also listens for realm
    servers in another thread to keep an up to date list of available servers.

    As the intern containers for logged in accounts and realms are accessed and
    updated from other thread, the server contains a lock for each shared
    object, including the sockets used by other thread, e.g. by the realm
    listener function.
    """

    # Hardcoded values, change that TODO
    CLIENTS_HOST = "0.0.0.0"
    CLIENTS_PORT = 3724
    REALMS_HOST = "127.0.0.1"
    REALMS_PORT = 3725
    BACKLOG_SIZE = 64
    REALM_MAX_UPDATE_TIME = 120

    def __init__(self):
        self.clients_socket = None
        self.realms_socket = None
        self.realms_socket_lock = threading.Lock()
        self.logged_in = {}
        self.logged_in_lock = threading.Lock()
        self.realms = {}
        self.realms_lock = threading.Lock()
        self.shutdown_flag = threading.Event()

    def start(self):
        LOG.info("Starting login server")
        self._start_listening()

        simple_thread(self._accept_realm_connections)
        self._accept_client_connections()

        self.shutdown_flag.set()
        self._stop_listening()
        LOG.info("Login server stopped.")

    def _start_listening(self):
        """ Start listening with non-blocking sockets, to still capture
        Windows signals. """
        self.realms_socket = socket.socket()
        self.realms_socket.settimeout(1)
        address = (LoginServer.REALMS_HOST, LoginServer.REALMS_PORT)
        self.realms_socket.bind(address)
        self.realms_socket.listen(LoginServer.BACKLOG_SIZE)

        self.clients_socket = socket.socket()
        self.clients_socket.settimeout(1)
        address = (LoginServer.CLIENTS_HOST, LoginServer.CLIENTS_PORT)
        self.clients_socket.bind(address)
        self.clients_socket.listen(LoginServer.BACKLOG_SIZE)

    def _accept_client_connections(self):
        """ Accept incoming clients connections until manual interruption. """
        try:
            while not self.shutdown_flag.is_set():
                self._try_accept_client_connection()
        except KeyboardInterrupt:
            LOG.info("KeyboardInterrupt received, stop accepting clients.")

    def _try_accept_client_connection(self):
        try:
            connection, address = self.clients_socket.accept()
            self._handle_client_connection(connection, address)
        except socket.timeout:
            pass

    def _handle_client_connection(self, connection, address):
        """ Start another thread to securely handle the client connection. """
        LOG.info("Accepting client connection from " + str(address))
        login_connection = LoginConnection(self, connection, address)
        simple_thread(login_connection.handle_connection)

    def _accept_realm_connections(self):
        """ Accept incoming realm connections forever, so this has to run in
        another thread. """
        while not self.shutdown_flag.is_set():
            with self.realms_socket_lock:
                try:
                    connection, address = self.realms_socket.accept()
                    self._handle_realm_connection(connection, address)
                except socket.timeout:
                    pass

    def _handle_realm_connection(self, connection, address):
        """ Start another thread to securely handle the realm connection. """
        LOG.debug("Accepting realm connection from " + str(address))
        realm_connection = RealmConnection(self, connection, address)
        simple_thread(realm_connection.handle_connection)

    def maintain_realm_list(self):
        """ Maintain realmlist by removing realms not updated for a while. """
        with self.realms_lock:
            to_remove = []
            for realm in self.realms:
                update_delay = time.time() - self.realms[realm]["last_update"]
                if update_delay > LoginServer.REALM_MAX_UPDATE_TIME:
                    to_remove.append(realm)
                    LOG.debug("Realm " + realm + " down, removed from list.")
            for realm_to_remove in to_remove:
                del self.realms[realm_to_remove]

    def _stop_listening(self):
        with self.realms_socket_lock:
            self.realms_socket.close()
            self.realms_socket = None

        self.clients_socket.close()
        self.clients_socket = None

    def get_account(self, account_name):
        return AccountManager.get_account(account_name)

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

    def get_realm_list(self):
        self.maintain_realm_list()
        with self.realms_lock:
            realm_list_copy = self.realms.copy()
        return realm_list_copy
