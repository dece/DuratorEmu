""" Represent states of the world connection automaton. """

from enum import Enum


class WorldConnectionState(Enum):

    INIT     = 0
    ERROR    = 1
    AUTH_OK  = 2
    IN_WORLD = 3
