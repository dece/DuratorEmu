import os
from struct import Struct

from durator.common.connection_automaton import ConnectionAutomaton
from durator.world.auth_session import AuthSessionHandler
from durator.world.char_selection.char_create import CharCreateHandler
from durator.world.char_selection.char_delete import CharDeleteHandler
from durator.world.char_selection.char_enum import CharEnumHandler
from durator.world.opcodes import OpCode
from durator.world.ping import PingHandler
from durator.world.world_connection_state import WorldConnectionState
from durator.world.world_packet import WorldPacket
from pyshgck.format import dump_data
from pyshgck.logger import LOG


class WorldConnection(ConnectionAutomaton):
    """ Handle the communication between a client and the world server. """

    AUTH_CHALLENGE_BIN = Struct("<I")

    LEGAL_OPS = {
        WorldConnectionState.INIT:    [ OpCode.CMSG_AUTH_SESSION ],
        WorldConnectionState.ERROR:   [ ],
        WorldConnectionState.AUTH_OK: [ OpCode.CMSG_CHAR_ENUM
                                      , OpCode.CMSG_CHAR_CREATE
                                      , OpCode.CMSG_CHAR_DELETE ]
    }

    UNMANAGED_OPS = [
        OpCode.CMSG_PING
    ]

    OP_HANDLERS = {
        OpCode.CMSG_AUTH_SESSION: AuthSessionHandler,
        OpCode.CMSG_CHAR_ENUM:    CharEnumHandler,
        OpCode.CMSG_CHAR_CREATE:  CharCreateHandler,
        OpCode.CMSG_CHAR_DELETE:  CharDeleteHandler,
        OpCode.CMSG_PING:         PingHandler
    }

    INIT_STATE       = WorldConnectionState.INIT
    END_STATES       = [ WorldConnectionState.ERROR ]
    MAIN_ERROR_STATE = WorldConnectionState.ERROR

    def __init__(self, server, connection):
        super().__init__(connection)
        self.server = server
        self.auth_seed = int.from_bytes(os.urandom(4), "little")
        self.account = None
        self.session_cipher = None

    def _send_packet(self, world_packet):
        print(">>>")
        print(dump_data(world_packet.data), end = "")
        ready_packet = world_packet.to_socket(self.session_cipher)
        self.socket.sendall(ready_packet)

    def _recv_packet(self):
        return WorldPacket.from_socket(self.socket, self.session_cipher)

    def _parse_packet(self, packet):
        return packet.opcode, packet.data

    def _actions_before_main_loop(self):
        LOG.debug("Sending auth challenge to setup session cipher.")
        self._send_auth_challenge()

    def _send_auth_challenge(self):
        packet_data = self.AUTH_CHALLENGE_BIN.pack(self.auth_seed)
        packet = WorldPacket(packet_data)
        packet.opcode = OpCode.SMSG_AUTH_CHALLENGE
        self._send_packet(packet)

    def _actions_after_main_loop(self):
        # Placeholder
        LOG.debug("World connection stopped handling packets.")
        while True:
            data = self.socket.recv(1024)
            print(dump_data(data), end = "")
