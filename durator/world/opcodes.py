""" Opcodes used to communicate between client and server.

There are deliberately few opcodes written below, because I don't want to
clutter this enum with opcodes I will never handle because they will likely not
appear within the goal usages of this emulator. Most of them come from CMangos.
"""

from enum import Enum


class OpCode(Enum):

    CMSG_CHAR_CREATE = 0x036
    CMSG_CHAR_ENUM   = 0x037
    CMSG_CHAR_DELETE = 0x038
    SMSG_CHAR_CREATE = 0x03A
    SMSG_CHAR_ENUM   = 0x03B
    SMSG_CHAR_DELETE = 0x03C

    CMSG_PLAYER_LOGIN     = 0x03D
    SMSG_NEW_WORLD        = 0x03E
    SMSG_TRANSFER_PENDING = 0x03F
    SMSG_TRANSFER_ABORTED = 0x040

    CMSG_NAME_QUERY          = 0x050
    SMSG_NAME_QUERY_RESPONSE = 0x051

    CMSG_ITEM_QUERY_SINGLE            = 0x056
    CMSG_ITEM_QUERY_MULTIPLE          = 0x057
    SMSG_ITEM_QUERY_SINGLE_RESPONSE   = 0x058
    SMSG_ITEM_QUERY_MULTIPLE_RESPONSE = 0x059

    SMSG_UPDATE_OBJECT  = 0x0A9
    SMSG_DESTROY_OBJECT = 0x0AA

    MSG_MOVE_START_FORWARD  = 0x0B5
    MSG_MOVE_START_BACKWARD = 0x0B6
    MSG_MOVE_STOP           = 0x0B7

    MSG_MOVE_WORLDPORT_ACK = 0x0DC

    SMSG_TUTORIAL_FLAGS = 0x0FD

    CMSG_QUERY_TIME          = 0x1CE
    SMSG_QUERY_TIME_RESPONSE = 0x1CF

    CMSG_PING = 0x1DC
    SMSG_PONG = 0x1DD

    SMSG_AUTH_CHALLENGE = 0x1EC
    CMSG_AUTH_SESSION   = 0x1ED
    SMSG_AUTH_RESPONSE  = 0x1EE

    SMSG_COMPRESSED_UPDATE_OBJECT = 0x1F6

    MSG_LOOKING_FOR_GROUP = 0x1FF

    CMSG_GMTICKET_GETTICKET = 0x211
    SMSG_GMTICKET_GETTICKET = 0x212

    SMSG_LOGIN_VERIFY_WORLD = 0x236

    CMSG_SET_ACTIVE_MOVER = 0x26A

    MSG_QUERY_NEXT_MAIL_TIME = 0x284
