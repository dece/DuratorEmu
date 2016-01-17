import os
from struct import Struct

from durator.auth.account import AccountSessionManager
from durator.common.networking.connection_automaton import ConnectionAutomaton
from durator.config import DEBUG
from durator.world.handlers.ack.move_worldport import MoveWorldportAckHandler
from durator.world.handlers.auth_session import AuthSessionHandler
from durator.world.handlers.char_selection.char_create import CharCreateHandler
from durator.world.handlers.char_selection.char_delete import CharDeleteHandler
from durator.world.handlers.char_selection.char_enum import CharEnumHandler
from durator.world.handlers.game.player_login import PlayerLoginHandler
from durator.world.handlers.nop import NopHandler
from durator.world.handlers.ping import PingHandler
from durator.world.opcodes import OpCode
from durator.world.world_connection_state import WorldConnectionState
from durator.world.world_packet import WorldPacket
from pyshgck.format import dump_data
from pyshgck.logger import LOG


class WorldConnection(ConnectionAutomaton):
    """ Handle the communication between a client and the world server.

    The shared_data dict holds misc temporary values that can be of use for
    several handlers; anything living longer than a few seconds should probably
    be stored somewhere else. The account and the session cipher attributes are
    set only when the AuthSessionHandler succeeds (state AUTH_OK at least). The
    guid and character_data variables are set only when the PlayerLoginHandler
    verifies them.
    """

    AUTH_CHALLENGE_BIN = Struct("<I")

    LEGAL_OPS = {
        WorldConnectionState.INIT:     [ OpCode.CMSG_AUTH_SESSION ],
        WorldConnectionState.ERROR:    [ ],
        WorldConnectionState.AUTH_OK:  [ OpCode.CMSG_CHAR_ENUM
                                       , OpCode.CMSG_CHAR_CREATE
                                       , OpCode.CMSG_CHAR_DELETE
                                       , OpCode.CMSG_PLAYER_LOGIN ],
        WorldConnectionState.IN_WORLD: [ OpCode.CMSG_NAME_QUERY ]
    }

    UNMANAGED_OPS = [
        OpCode.CMSG_PING,
        OpCode.MSG_MOVE_WORLDPORT_ACK,
    ]

    OP_HANDLERS = {
        OpCode.CMSG_AUTH_SESSION:      AuthSessionHandler,
        OpCode.CMSG_CHAR_CREATE:       CharCreateHandler,
        OpCode.CMSG_CHAR_DELETE:       CharDeleteHandler,
        OpCode.CMSG_CHAR_ENUM:         CharEnumHandler,
        OpCode.CMSG_NAME_QUERY:        NopHandler,
        OpCode.CMSG_PING:              PingHandler,
        OpCode.CMSG_PLAYER_LOGIN:      PlayerLoginHandler,
        OpCode.MSG_MOVE_WORLDPORT_ACK: MoveWorldportAckHandler
    }

    INIT_STATE       = WorldConnectionState.INIT
    END_STATES       = [ WorldConnectionState.ERROR ]
    MAIN_ERROR_STATE = WorldConnectionState.ERROR

    def __init__(self, server, connection):
        super().__init__(connection)
        self.server = server
        self.shared_data = {}

        self.account = None
        self.session_cipher = None

        self.guid = -1
        self.character_data = None

    def send_packet(self, world_packet):
        if DEBUG:
            print(">>>")
            print(dump_data(world_packet.data), end = "")
        ready_packet = world_packet.to_socket(self.session_cipher)
        self.socket.sendall(ready_packet)

    def _recv_packet(self):
        try:
            return WorldPacket.from_socket(self.socket, self.session_cipher)
        except ConnectionResetError:
            LOG.info("Lost connection with " + self.account.name + ".")
            return None

    def _parse_packet(self, packet):
        return packet.opcode, packet.data

    def _actions_before_main_loop(self):
        LOG.debug("Sending auth challenge to setup session cipher.")
        self._send_auth_challenge()

    def _send_auth_challenge(self):
        auth_seed = int.from_bytes(os.urandom(4), "little")
        self.shared_data["auth_seed"] = auth_seed

        packet_data = self.AUTH_CHALLENGE_BIN.pack(auth_seed)
        packet = WorldPacket(packet_data)
        packet.opcode = OpCode.SMSG_AUTH_CHALLENGE
        self.send_packet(packet)

    def _actions_after_main_loop(self):
        LOG.debug("World connection stopped handling packets.")
        AccountSessionManager.delete_session(self.account)

        if DEBUG:
            LOG.debug("Debug mode: looping over received data.")
            try:
                while True:
                    data = self.socket.recv(1024)
                    print(dump_data(data), end = "")
            except ConnectionResetError:
                LOG.debug("Lost connection.")
