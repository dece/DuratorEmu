""" Represent states in the char selection process. """

from enum import Enum


class CharSelectionState(Enum):

    INIT           = 0
    ERROR          = 1
    SENT_AUTH_RESP = 2
