from enum import Enum


class OpCode(Enum):

    SMSG_AUTH_CHALLENGE = 0x1EC
    CMSG_AUTH_SESSION   = 0x1ED
    SMSG_AUTH_RESPONSE  = 0x1EE
