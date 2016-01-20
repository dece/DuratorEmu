""" Represent states of the world connection automaton. """

from enum import Enum


class WorldConnectionState(Enum):

    INIT     = 0  # Start state.
    ERROR    = 1  # End state.
    AUTH_OK  = 2  # Session cipher is up, client is at char screen.
    IN_WORLD = 3  # Player is in world
    LOGOUT   = 4  # End state, client is completely logged out.
