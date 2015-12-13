import socket
import threading
import time

from durator.auth.account import AccountManager, AccountSessionManager
from durator.auth.login_connection import LoginConnection
from durator.auth.realm_connection import RealmConnection
from pyshgck.concurrency import simple_thread
from pyshgck.logger import LOG


class LoginServer(object):
    """ Listen for clients and start a new thread for each connection.

    The LoginServer listens for clients (main socket) but also listens for realm
    servers in another thread to keep an up to date list of available servers.

    As the intern containers for logged in accounts and realms are accessed and
    updated from other thread, the server contains a lock for each shared
    object, including the sockets used by other thread, e.g. by the realm
    listener function.

    self.realms is dict mapping realm names to realm_state dicts. These dicts
    contains a ready RealmInfo_S "packet" to be send to clients, and a timestamp
    "last_update" of the last time it got updated by the remote world server.
    """

    # Hardcoded values, change that TODO
    CLIENTS_HOST          = "0.0.0.0"
    CLIENTS_PORT          = 3724
    REALMS_HOST           = "127.0.0.1"
    REALMS_PORT           = 3725
    BACKLOG_SIZE          = 64
    REALM_MAX_UPDATE_TIME = 120

    def __init__(self):
        self.clients_socket = None
        self.realms_socket = None
        self.logged_in = {}
        self.realms = {}
        self.shutdown_flag = threading.Event()

        self.locks = { attr: threading.Lock() for attr in
                       ["realms_socket", "realms", "logged_in"] }

    def start(self):
        LOG.info("Starting login server")
        self._clean_db()
        self._start_listening()

        simple_thread(self._accept_realm_connections)
        self._accept_client_connections()

        self.shutdown_flag.set()
        self._stop_listening()
        self._clean_db()
        LOG.info("Login server stopped.")

    def _clean_db(self):
        LOG.debug("Cleaning database")
        AccountSessionManager.delete_all_sessions()

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
        login_connection = LoginConnection(self, connection)
        simple_thread(login_connection.handle_connection)

    def _accept_realm_connections(self):
        """ Accept incoming realm connections forever, so this has to run in
        another thread. """
        while not self.shutdown_flag.is_set():
            with self.locks["realms_socket"]:
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

    def _stop_listening(self):
        with self.locks["realms_socket"]:
            self.realms_socket.close()
            self.realms_socket = None

        self.clients_socket.close()
        self.clients_socket = None

    def get_account(self, account_name):
        """ Return the account with that name. """
        return AccountManager.get_account(account_name)

    def accept_account_login(self, account, session_key):
        """ Accept the account login in the active sessions table. """
        AccountSessionManager.add_session(account, session_key)

    def get_account_session(self, account_name):
        """ Return the account session if it's logged in, None otherwise. """
        return AccountSessionManager.get_session(account_name)

    def get_realm_list(self):
        """ Return a copy of the realm states dict. """
        self._maintain_realm_list()
        with self.locks["realms"]:
            realm_list_copy = self.realms.copy()
        return realm_list_copy

    def _maintain_realm_list(self):
        """ Maintain realmlist by removing realms not updated for a while. """
        with self.locks["realms"]:
            to_remove = []
            for realm in self.realms:
                update_delay = time.time() - self.realms[realm]["last_update"]
                if update_delay > LoginServer.REALM_MAX_UPDATE_TIME:
                    to_remove.append(realm)
                    LOG.debug("Realm " + realm + " down, removed from list.")
            for realm_to_remove in to_remove:
                del self.realms[realm_to_remove]
