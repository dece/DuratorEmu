""" Represent the SRP connection process automaton states. """

from enum import Enum


class LoginConnectionState(Enum):

    INIT        = 0
    CLOSED      = 1
    SENT_CHALL  = 2
    SENT_PROOF  = 3
    RECON_CHALL = 4
    RECON_PROOF = 5
