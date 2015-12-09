from enum import Enum
import socket
import struct
import threading
import time

from pyshgck.concurrency import simple_thread
from pyshgck.logger import LOG


class Population(Enum):

    LOW     = 0
    AVERAGE = 1
    HIGH    = 2
    FULL    = 3

    def as_float(self):
        return float(self.value)


class WorldServer(object):

    DEFAULT_HOST = "127.0.0.1"
    DEFAULT_PORT = 13250

    def __init__(self):
        self.name = "CYRIXCYRIXCYRIXCYRIX"
        self.population = Population.EMPTY
        self.host = WorldServer.DEFAULT_HOST
        self.port = WorldServer.DEFAULT_PORT

        self.login_server_socket = None
        self.shutdown_flag = threading.Event()

    def start(self):
        LOG.info("Starting world server " + self.name)
        simple_thread(self._handle_login_server_connection)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            LOG.info("KeyboardInterrupt received, stopping server.")
            self.shutdown_flag.set()

    def _handle_login_server_connection(self):
        """ Update forever the realm state to the login server. """
        while not self.shutdown_flag.is_set():
            LOG.debug("Sending heartbeat to login server")
            state_packet = self._get_state_packet()
            socket_is_opened = self._open_login_server_socket()
            if socket_is_opened:
                self.login_server_socket.sendall(state_packet)
            self._close_login_server_socket()
            time.sleep(30)

    def _get_state_packet(self):
        packet = b""
        name = self.name.encode("ascii")
        packet += int.to_bytes(len(name), 1, "little")
        packet += name
        packet += struct.pack("f", self.population.as_float())
        address = (self.host + ":" + str(self.port)).encode("ascii")
        packet += int.to_bytes(len(address), 1, "little")
        packet += address
        packet = int.to_bytes(len(packet), 1, "little") + packet
        return packet

    def _open_login_server_socket(self):
        self.login_server_socket = socket.socket()
        # Hardcoded login server address, change that
        address = ("127.0.0.1", 3725)
        try:
            self.login_server_socket.connect(address)
            return True
        except ConnectionError as exc:
            LOG.error("Couldn't join login server! " + str(exc))
            return False

    def _close_login_server_socket(self):
        self.login_server_socket.close()
        self.login_server_socket = None
