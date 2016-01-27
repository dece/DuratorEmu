import socket
import threading
import time

from durator.auth.login_connection import LoginConnection
from durator.auth.realm_connection import RealmConnection
from durator.common.account.managers import AccountSessionManager
from durator.config import CONFIG
from pyshgck.concurrency import simple_thread
from pyshgck.logger import LOG


class LoginServer(object):
    """ Listen for clients and start a new thread for each connection.

    The LoginServer listens for clients (main socket) but also listens for realm
    servers in another thread to keep an up to date list of available servers.

    Note that the config contains information for only one realm so several
    realms should be installed on different machines with different config
    files. This sucks and should be fixed later.

    As the intern containers for logged in accounts and realms are accessed and
    updated from other thread, the server contains a lock for each shared
    object, including the sockets used by other thread, e.g. by the realm
    listener function. This may suck as this packet contains user specific data.

    self.realms is dict mapping realm names to realm_state dicts. These dicts
    contains a ready RealmInfo_S "packet" to be send to clients, and a timestamp
    "last_update" of the last time it got updated by the remote world server.
    """

    CLIENTS_HOST          = CONFIG["login"]["clients_conn_hostname"]
    CLIENTS_PORT          = int(CONFIG["login"]["clients_conn_port"])
    REALMS_HOST           = CONFIG["login"]["realm_conn_hostname"]
    REALMS_PORT           = int(CONFIG["login"]["realm_conn_port"])
    BACKLOG_SIZE          = 64
    REALM_MAX_UPDATE_TIME = int(CONFIG["login"]["realm_max_update_time"])

    def __init__(self):
        self.clients_socket = None
        self.realms_socket = None
        self.realms = {}
        self.shutdown_flag = threading.Event()

        self.locks = { attr: threading.Lock() for attr in
                       ["realms_socket", "realms"] }

    def start(self):
        LOG.info("Starting login server")
        self._start_listen()

        simple_thread(self._accept_realms)
        self._accept_clients()

        self.shutdown_flag.set()
        self._stop_listen()
        AccountSessionManager.delete_all_sessions()
        LOG.info("Login server stopped.")

    def _start_listen(self):
        """ Start listening with non-blocking sockets, to still capture
        Windows signals. """
        self._listen_clients()
        self._listen_realms()

    def _stop_listen(self):
        self._stop_listen_clients()
        self._stop_listen_realms()

    #------------------------------
    # Clients connection
    #------------------------------

    def _listen_clients(self):
        self.clients_socket = socket.socket()
        self.clients_socket.settimeout(1)
        address = (self.CLIENTS_HOST, self.CLIENTS_PORT)
        self.clients_socket.bind(address)
        self.clients_socket.listen(self.BACKLOG_SIZE)

    def _accept_clients(self):
        """ Accept incoming clients connections until manual interruption. """
        try:
            while not self.shutdown_flag.is_set():
                self._try_accept_client()
        except KeyboardInterrupt:
            LOG.info("KeyboardInterrupt received, stop accepting clients.")

    def _try_accept_client(self):
        try:
            connection, address = self.clients_socket.accept()
            self._handle_client(connection, address)
        except socket.timeout:
            pass

    def _handle_client(self, connection, address):
        """ Start another thread to securely handle the client connection. """
        LOG.info("Accepting client connection from " + str(address))
        login_connection = LoginConnection(self, connection)
        simple_thread(login_connection.handle_connection)

    def accept_account_login(self, account, session_key):
        """ Accept the account login in the active sessions table. """
        AccountSessionManager.add_session(account, session_key)

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
                if update_delay > self.REALM_MAX_UPDATE_TIME:
                    to_remove.append(realm)
                    LOG.debug("Realm " + realm + " down, removed from list.")
            for realm_to_remove in to_remove:
                del self.realms[realm_to_remove]

    def _stop_listen_clients(self):
        self.clients_socket.close()
        self.clients_socket = None

    #------------------------------
    # World servers connection
    #------------------------------

    def _listen_realms(self):
        self.realms_socket = socket.socket()
        self.realms_socket.settimeout(1)
        address = (self.REALMS_HOST, self.REALMS_PORT)
        self.realms_socket.bind(address)
        self.realms_socket.listen(self.BACKLOG_SIZE)

    def _accept_realms(self):
        """ Accept incoming realm connections forever, so this has to run in
        another thread. """
        while not self.shutdown_flag.is_set():
            with self.locks["realms_socket"]:
                try:
                    connection, address = self.realms_socket.accept()
                    self._handle_realm(connection, address)
                except socket.timeout:
                    pass

    def _handle_realm(self, connection, address):
        """ Start another thread to securely handle the realm connection. """
        realm_connection = RealmConnection(self, connection, address)
        simple_thread(realm_connection.handle_connection)

    def _stop_listen_realms(self):
        with self.locks["realms_socket"]:
            self.realms_socket.close()
            self.realms_socket = None
