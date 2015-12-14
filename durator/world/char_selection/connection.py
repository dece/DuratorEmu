import os
from struct import Struct

from durator.common.connection_automaton import ConnectionAutomaton
from durator.world.char_selection.auth_session import AuthSessionHandler
from durator.world.char_selection.char_enum import CharEnumHandler
from durator.world.char_selection.connection_state import CharSelectionState
from durator.world.opcodes import OpCode
from durator.world.ping import PingHandler
from durator.world.world_packet import WorldPacket
from pyshgck.format import dump_data
from pyshgck.logger import LOG


class CharSelectionConnection(ConnectionAutomaton):
    """ Handle a client connection during the char selection process.

    During this step, the server and the client communicate about character
    listing, character creation, etc. The server has to start the dialog with
    an auth challenge. If the authentication goes well, this connection then
    holds the client account and the session cipher needed to communicate with
    the client.
    """

    AUTH_CHALLENGE_BIN = Struct("<I")

    LEGAL_OPS = {
        CharSelectionState.INIT:    [ OpCode.CMSG_AUTH_SESSION ],
        CharSelectionState.ERROR:   [ ],
        CharSelectionState.AUTH_OK: [ OpCode.CMSG_CHAR_ENUM ]
    }

    UNMANAGED_OPS = [
        OpCode.CMSG_PING
    ]

    OP_HANDLERS = {
        OpCode.CMSG_AUTH_SESSION: AuthSessionHandler,
        OpCode.CMSG_CHAR_ENUM:    CharEnumHandler
        OpCode.CMSG_PING:         PingHandler
    }

    INIT_STATE       = CharSelectionState.INIT
    END_STATES       = [ CharSelectionState.ERROR ]
    MAIN_ERROR_STATE = CharSelectionState.ERROR

    def __init__(self, world_connection, socket):
        self.world_conn = world_connection
        super().__init__(socket)
        self.auth_seed = int.from_bytes(os.urandom(4), "little")
        self.account = None
        self.session_cipher = None

    def _send_packet(self, world_packet):
        print(">>>")
        print(dump_data(world_packet.data), end = "")
        ready_packet = world_packet.to_socket(self.session_cipher)
        print(dump_data(ready_packet), end = "")
        self.socket.sendall(ready_packet)

    def _recv_packet(self):
        return WorldPacket.from_socket(self.socket, self.session_cipher)

    def _parse_packet(self, packet):
        """ Return opcode and packet content. """
        return packet.opcode, packet.data

    def _actions_before_main_loop(self):
        LOG.debug("Entering the char selection process")
        self._send_auth_challenge()

    def _send_auth_challenge(self):
        packet_data = self.AUTH_CHALLENGE_BIN.pack(self.auth_seed)
        packet = WorldPacket(packet_data)
        packet.opcode = OpCode.SMSG_AUTH_CHALLENGE
        self._send_packet(packet)
