from durator.world.opcodes import Opcode
from durator.world.char_selection import CharSelectionProcess
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
        # while True:
        #     data = self._get_whole_packet()
        #     if data is None:
        #         return
        #     print("<<<")
        #     print(dump_data(data), end = "")

    # def _get_whole_packet(self):
    #     data = self.socket.recv(1024)
    #     if not data:
    #         return None
    #     # packet_size = data[0]
    #     # while len(data[1:]) < packet_size:
    #     #     data_part = self.socket.recv(1024)
    #     #     if not data_part:
    #     #         return None
    #     #     data += data_part

    def _process_char_selection(self):
        char_selection_process = CharSelectionProcess(self.socket)
        char_selection_process.process()
