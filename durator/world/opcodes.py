from enum import Enum


class Opcode(Enum):

    SMSG_AUTH_CHALLENGE = 0x1EC
    SMSG_AUTH_RESPONSE  = 0x1EE
