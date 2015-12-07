""" Opcodes and other constant values used during the auth process. """

from enum import Enum


class LoginOpCodes(Enum):
    """ Opcodes used during the login process """

    LOGIN_CHALL   = 0x00
    LOGIN_PROOF   = 0x01
    RECON_CHALL   = 0x02
    RECON_PROOF   = 0x03
    REALMLIST     = 0x10
    XFER_INITIATE = 0x30
    XFER_DATA     = 0x31


class LoginResults(Enum):
    """ Error codes in server packets """

    SUCCESS               = 0x00
    FAIL_1                = 0x01
    FAIL_2                = 0x02
    FAIL_BANNED           = 0x03
    FAIL_UNKNOWN_ACCOUNT  = 0x04
    FAIL_WRONG_PASSWORD   = 0x05
    FAIL_ALREADY_ONLINE   = 0x06
    FAIL_NO_TIME          = 0x07
    FAIL_DB_BUSY          = 0x08
    FAIL_VERSION_INVALID  = 0x09
    FAIL_VERSION_UPDATE   = 0x0A
    FAIL_INVALID_SERVER   = 0x0B
    FAIL_SUSPENDED        = 0x0C
    FAIL_NOACCESS         = 0x0D
