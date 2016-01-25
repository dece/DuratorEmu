import socket
import threading
import time

from durator.config import CONFIG
from durator.world.game.manager.chat import ChatManager
from durator.world.game.manager.object import ObjectManager
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

        self.world_connections = []
        self.world_connections_lock = threading.Lock()
        self.object_manager = ObjectManager(self)
        self.chat_manager = ChatManager(self)

        self.shutdown_flag = threading.Event()

    def _create_realm(self):
        realm_name = CONFIG["realm"]["name"]
        realm_address = "{}:{}".format(self.hostname, self.port)
        realm_id = RealmId(int(CONFIG["realm"]["id"]))
        self.realm = Realm(realm_name, realm_address, realm_id)

    def start(self):
        LOG.info("Starting world server " + self.realm.name)
        self._listen_clients()

        simple_thread(self._handle_login_server_connection)
        self._accept_clients()

        self.shutdown_flag.set()
        self._stop_listen_clients()
        LOG.info("World server stopped.")

    #------------------------------
    # Clients connection
    #------------------------------

    def _listen_clients(self):
        self.clients_socket = socket.socket()
        self.clients_socket.settimeout(1)
        clients_address = (self.hostname, self.port)
        self.clients_socket.bind(clients_address)
        self.clients_socket.listen(WorldServer.BACKLOG_SIZE)

    def _stop_listen_clients(self):
        self.clients_socket.close()
        self.clients_socket = None

    def _accept_clients(self):
        """ Regularly try to access client while looking for interrupts. """
        try:
            while True:
                self._try_accept_client()
        except KeyboardInterrupt:
            LOG.info("KeyboardInterrupt received, stop accepting clients.")

    def _try_accept_client(self):
        """ Accept a client connection or timeout if there aren't any. """
        try:
            connection, address = self.clients_socket.accept()
            self._handle_client(connection, address)
        except socket.timeout:
            pass

    def _handle_client(self, connection, address):
        """ Start the threaded WorldConnection and add it to the local list. """
        LOG.info("Accepting client connection from " + str(address))
        world_connection = WorldConnection(self, connection)

        with self.world_connections_lock:
            self.world_connections.append(world_connection)

        simple_thread(world_connection.handle_connection)

    #------------------------------
    # Login server connection
    #------------------------------

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

    #------------------------------
    # Server utilities
    #------------------------------

    def broadcast(self, packet, state = None, guids = None):
        """ Send a WorldPacket to all eligible WorldConnection. """
        with self.world_connections_lock:
            for connection in self.world_connections:
                eligible = WorldServer._get_broadcast_eligibility(
                    connection, state, guids
                )
                if eligible:
                    connection.outgoing_queue.put(packet)

    @staticmethod
    def _get_broadcast_eligibility(connection, state, guids):
        """ Return whether a connection is eligible to receive a broadcast.

        If state is provided, send packet only WorldConnections in that state.
        If guids is provided, send packet only to players in that GUID list.
        """
        state_condition = ( state is None
                            or connection.state == state )
        guid_condition = ( guids is None
                           or ( connection.player
                                and connection.player.guid in guids ) )
        eligible = state_condition and guid_condition
        return eligible
