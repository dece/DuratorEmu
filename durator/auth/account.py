from enum import Enum

from durator.auth.srp import Srp


class Account(object):
    """ Account with SRP data.
    
    Attributes:
        name: str, account name
        status: Status, determine if that account is usable or not
        srp_salt: bytes, length 32
        srp_verifier: int, computed from account and pass
    """

    class Status(Enum):
        NOT_READY = 0
        OK        = 1
        BANNED    = 2
        SUSPENDED = 3

    def __init__(self, name):
        self.name = name
        self.status = Account.Status.NOT_READY
        self.srp_salt = b""
        self.srp_verifier = 0

    def can_log(self):
        return self.status == Account.Status.OK

    @staticmethod
    def get_dummy_account(name):
        """ Get a dummy testing account, using account name as a password. """
        account = Account(name)
        Srp.generate_account_srp_data(account, account.name)
        account.status = Account.Status.OK
        return account
