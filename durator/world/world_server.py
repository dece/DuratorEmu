import socket
import threading
import time

from durator.config import CONFIG
from durator.world.game.object_manager import ObjectManager
from durator.world.realm import Realm, RealmId, RealmFlags, RealmPopulation
from durator.world.world_connection import WorldConnection
from pyshgck.concurrency import simple_thread
from pyshgck.logger import LOG


class WorldServer(object):
    """ World server accepting connections from clients.

    At this point in development, it is the world server that creates and
    registers to the database the realm it hosts. In the long run though, it
    would probably be better to separate them and that a world server gets
    initialized with an already existing realm.
    """

    BACKLOG_SIZE = 64
    LOGIN_SERVER_HEARTBEAT_RATE = int(CONFIG["login"]["realm_heartbeat_time"])

    def __init__(self):
        self.hostname = CONFIG["realm"]["hostname"]
        self.port = int(CONFIG["realm"]["port"])
        self.realm = None
        self.population = RealmPopulation.LOW
        self._create_realm()

        self.login_server_socket = None
        self.clients_socket = None

        self.object_manager = ObjectManager()

        self.shutdown_flag = threading.Event()

    def start(self):
        LOG.info("Starting world server " + self.realm.name)
        self._start_listening_for_clients()

        simple_thread(self._handle_login_server_connection)
        self._accept_client_connections()

        self.shutdown_flag.set()
        self._stop_listening_for_clients()
        LOG.info("World server stopped.")

    def _create_realm(self):
        realm_name = CONFIG["realm"]["name"]
        realm_address = "{}:{}".format(self.hostname, self.port)
        realm_id = RealmId(int(CONFIG["realm"]["id"]))
        self.realm = Realm(realm_name, realm_address, realm_id)

    def _start_listening_for_clients(self):
        self.clients_socket = socket.socket()
        self.clients_socket.settimeout(1)
        clients_address = (self.hostname, self.port)
        self.clients_socket.bind(clients_address)
        self.clients_socket.listen(WorldServer.BACKLOG_SIZE)

    def _stop_listening_for_clients(self):
        self.clients_socket.close()
        self.clients_socket = None

    def _accept_client_connections(self):
        try:
            while True:
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
        LOG.info("Accepting client connection from " + str(address))
        world_connection = WorldConnection(self, connection)
        simple_thread(world_connection.handle_connection)

    def _handle_login_server_connection(self):
        """ Update forever the realm state to the login server. """
        while not self.shutdown_flag.is_set():
            state_packet = self.realm.get_state_packet(
                RealmFlags.NORMAL, self.population
            )

            self._open_login_server_socket()
            if self.login_server_socket:
                self.login_server_socket.sendall(state_packet)
                self._close_login_server_socket()

            time.sleep(self.LOGIN_SERVER_HEARTBEAT_RATE)

    def _open_login_server_socket(self):
        """ Open the login server socket, or set it to None if it couldn't
        connect properly. """
        self.login_server_socket = socket.socket()
        login_server_address = ( CONFIG["login"]["realm_conn_hostname"]
                               , int(CONFIG["login"]["realm_conn_port"]) )
        try:
            self.login_server_socket.connect(login_server_address)
        except ConnectionError as exc:
            LOG.error("Couldn't join login server! " + str(exc))
            self.login_server_socket = None

    def _close_login_server_socket(self):
        self.login_server_socket.close()
        self.login_server_socket = None
