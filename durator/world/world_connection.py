from durator.world.opcodes import Opcode
from durator.world.char_selection import CharSelectionProcess
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
        char_selection_process = CharSelectionProcess(self, self.socket)
        char_selection_process.process()
