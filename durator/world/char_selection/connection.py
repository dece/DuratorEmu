import os
from struct import Struct

from durator.common.connection_automaton import ConnectionAutomaton
from durator.world.char_selection.auth_session import AuthSessionHandler
from durator.world.char_selection.connection_state import CharSelectionState
from durator.world.opcodes import OpCode
from durator.world.world_packet import WorldPacket
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

    def __init__(self, world_connection, socket):
        self.world_conn = world_connection
        super().__init__(socket)
        self.auth_seed = int.from_bytes(os.urandom(4), "little")

    def _send_packet(self, data):
        """ Send data prepended with the data size in big endian. """
        packet = CharSelectionConnection.PACKET_SIZE_BIN.pack(len(data)) + data
        self.socket.sendall(packet)

    def _recv_packet(self):
        return WorldPacket.from_socket(self.socket)

    def _parse_packet(self, packet):
        """ Return opcode and packet content. """
        return packet.opcode, packet.data

    def _actions_before_main_loop(self):
        LOG.debug("Entering the char selection process")
        self._send_auth_challenge()

    def _send_auth_challenge(self):
        packet = CharSelectionConnection.AUTH_CHALLENGE_BIN.pack(
            OpCode.SMSG_AUTH_CHALLENGE.value,
            self.auth_seed
        )
        self._send_packet(packet)
