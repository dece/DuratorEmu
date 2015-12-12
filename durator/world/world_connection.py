from durator.world.char_selection.connection import CharSelectionConnection
from pyshgck.format import dump_data
from pyshgck.logger import LOG


class WorldConnection(object):
    """ Handle the communication between a client and the world server. """

    def __init__(self, server, connection, address):
        self.server = server
        self.socket = connection
        self.address = address

    def handle_connection(self):
        self._process_char_selection()

    def _process_char_selection(self):
        char_selection = CharSelectionConnection(self, self.socket)
        char_selection.process()
        LOG.debug("Char selection done, we should handle to rest now.")

        # Placeholder
        while True:
            data = self.socket.recv(1024)
            print(dump_data(data), end = "")
