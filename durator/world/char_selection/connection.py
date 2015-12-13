import os
from struct import Struct

from durator.common.connection_automaton import ConnectionAutomaton
from durator.world.char_selection.auth_session import AuthSessionHandler
from durator.world.char_selection.connection_state import CharSelectionState
from durator.world.opcodes import OpCode
from pyshgck.format import dump_data
from pyshgck.logger import LOG


class CharSelectionConnection(ConnectionAutomaton):
    """ Handle a client connection during the char selection process.

    During this step, the server and the client communicate about character
    listing, character creation, etc. The server has to start the dialog with
    an auth challenge.
    """

    PACKET_SIZE_BIN    = Struct(">H")
    AUTH_CHALLENGE_BIN = Struct("<HI")

    LEGAL_OPS = {
        CharSelectionState.INIT: [ OpCode.CMSG_AUTH_SESSION ]
    }

    OP_HANDLERS = {
        OpCode.CMSG_AUTH_SESSION: AuthSessionHandler
    }

    INIT_STATE       = CharSelectionState.INIT
    END_STATES       = [ CharSelectionState.ERROR ]
    MAIN_ERROR_STATE = CharSelectionState.ERROR

    def __init__(self, world_server, connection):
        self.world_server = world_server
        super().__init__(connection)
        self.auth_seed = int.from_bytes(os.urandom(4), "little")

    def _send_packet(self, data):
        """ Send data prepended with the data size in big endian. """
        packet = CharSelectionConnection.PACKET_SIZE_BIN.pack(len(data)) + data
        self.socket.sendall(packet)

    def _recv_packet(self):
        """ Receive a full-sized packet, and return it without the size uint16.

        Ok so if two packets get packed in the same TCP frame, we might get them
        concatenated, right? The fact that the data size prepended is of various
        size and endianness sucks, but if I find some consistency later I might
        write a generic packet handler that'll handle all that.
        """
        data = b""
        while True:
            data_part = self.socket.recv(1024)
            if not data:
                return None
            data += data_part

            if len(data) < 2:
                continue

            packet_size = int.from_bytes(data[0:2], "big")
            if len(data[2:]) >= packet_size:
                data = data[2 : 2+packet_size]
                print(dump_data(data), end = "")
                return data

    def _parse_packet(self, packet):
        """ Return opcode and packet content. """
        pass #DO ET

    def _actions_before_main_loop(self):
        LOG.debug("Entering the char selection process")
        self._send_auth_challenge()

    def _send_auth_challenge(self):
        packet = CharSelectionConnection.AUTH_CHALLENGE_BIN.pack(
            OpCode.SMSG_AUTH_CHALLENGE.value,
            self.auth_seed
        )
        self._send_packet(packet)
