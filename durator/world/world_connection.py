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
from durator.world.handlers.game.account_data import RequestAccountDataHandler
from durator.world.handlers.game.logout import LogoutRequestHandler
from durator.world.handlers.game.movement import MovementHandler
from durator.world.handlers.game.name_query import NameQueryHandler
from durator.world.handlers.game.player_login import PlayerLoginHandler
from durator.world.handlers.game.time_query import TimeQueryHandler
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
                                       , OpCode.CMSG_PLAYER_LOGIN ]
    }

    UNMANAGED_OPS = [
        OpCode.CMSG_PING
    ]

    UNMANAGED_STATES = [
        WorldConnectionState.IN_WORLD
    ]

    OP_HANDLERS = {
        # Handled opcodes
        OpCode.CMSG_CHAR_CREATE:            CharCreateHandler,
        OpCode.CMSG_CHAR_ENUM:              CharEnumHandler,
        OpCode.CMSG_CHAR_DELETE:            CharDeleteHandler,
        OpCode.CMSG_PLAYER_LOGIN:           PlayerLoginHandler,
        OpCode.CMSG_LOGOUT_REQUEST:         LogoutRequestHandler,
        OpCode.CMSG_NAME_QUERY:             NameQueryHandler,
        OpCode.MSG_MOVE_START_FORWARD:      MovementHandler,
        OpCode.MSG_MOVE_START_BACKWARD:     MovementHandler,
        OpCode.MSG_MOVE_STOP:               MovementHandler,
        OpCode.MSG_MOVE_START_STRAFE_LEFT:  MovementHandler,
        OpCode.MSG_MOVE_START_STRAFE_RIGHT: MovementHandler,
        OpCode.MSG_MOVE_STOP_STRAFE:        MovementHandler,
        OpCode.MSG_MOVE_JUMP:               MovementHandler,
        OpCode.MSG_MOVE_START_TURN_LEFT:    MovementHandler,
        OpCode.MSG_MOVE_START_TURN_RIGHT:   MovementHandler,
        OpCode.MSG_MOVE_STOP_TURN:          MovementHandler,
        OpCode.MSG_MOVE_START_PITCH_UP:     MovementHandler,
        OpCode.MSG_MOVE_START_PITCH_DOWN:   MovementHandler,
        OpCode.MSG_MOVE_STOP_PITCH:         MovementHandler,
        OpCode.MSG_MOVE_SET_RUN_MODE:       MovementHandler,
        OpCode.MSG_MOVE_SET_WALK_MODE:      MovementHandler,
        OpCode.MSG_MOVE_FALL_LAND:          MovementHandler,
        OpCode.MSG_MOVE_SET_FACING:         MovementHandler,
        OpCode.MSG_MOVE_WORLDPORT_ACK:      MoveWorldportAckHandler,
        OpCode.MSG_MOVE_HEARTBEAT:          MovementHandler,
        OpCode.CMSG_QUERY_TIME:             TimeQueryHandler,
        OpCode.CMSG_PING:                   PingHandler,
        OpCode.CMSG_AUTH_SESSION:           AuthSessionHandler,
        OpCode.CMSG_REQUEST_ACCOUNT_DATA:   RequestAccountDataHandler,

        # Unhandled opcodes
        OpCode.CMSG_ITEM_QUERY_SINGLE:            NopHandler,
        OpCode.CMSG_ITEM_QUERY_MULTIPLE:          NopHandler,
        OpCode.SMSG_ITEM_QUERY_SINGLE_RESPONSE:   NopHandler,
        OpCode.SMSG_ITEM_QUERY_MULTIPLE_RESPONSE: NopHandler,
        OpCode.MSG_LOOKING_FOR_GROUP:             NopHandler,
        OpCode.CMSG_UPDATE_ACCOUNT_DATA:          NopHandler,  # temp
        OpCode.CMSG_GMTICKET_GETTICKET:           NopHandler,
        OpCode.CMSG_SET_ACTIVE_MOVER:             NopHandler,
        OpCode.MSG_QUERY_NEXT_MAIL_TIME:          NopHandler
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

        self.player = None

    def send_packet(self, world_packet):
        if DEBUG:
            print(">>>", world_packet.opcode)
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
        packet = WorldPacket(OpCode.SMSG_AUTH_CHALLENGE, packet_data)
        self.send_packet(packet)

    def _actions_after_main_loop(self):
        LOG.debug("WorldConnection: session ended.")
        AccountSessionManager.delete_session(self.account)
