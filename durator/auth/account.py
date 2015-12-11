from enum import Enum

from peewee import Model, CharField, IntegerField, BlobField, BigIntegerField

from durator.auth.srp import Srp
from durator.db.database import DB, db_connection


class Account(Model):
    """ Account with SRP data.

    Attributes:
        name: account name
        status: AccountStatus, determine if that account is usable or not
        srp_salt: 32-byte SRP salt
        srp_verifier: big int computed from account and pass
    """

    name = CharField(max_length = 64)
    status = IntegerField()
    srp_salt = BlobField()
    srp_verifier = BigIntegerField()

    class Meta(object):

        database = DB

    def is_valid(self):
        return self.status == AccountStatus.VALID.value


class AccountStatus(Enum):
    """ Determine if an account can log in (VALID) or not (any other value). """

    NOT_READY = 0
    VALID     = 1
    BANNED    = 2
    SUSPENDED = 3


class AccountManager(object):
    """ Manage the accounts in the database. """

    @staticmethod
    @db_connection
    def create_account(account_name, password):
        """ Create a valid account and add it to the database. """
        account = Account(
            name = account_name, status = AccountStatus.NOT_READY.value
        )
        Srp.generate_account_srp_data(account, password)
        account.status = AccountStatus.VALID.value
        account.save()
        return account

    @staticmethod
    @db_connection
    def get_account(account_name):
        """ Return the account from the database if it exists, or None. """
        try:
            return Account.get(Account.name == account_name)
        except Account.DoesNotExist:
            return None

    @staticmethod
    def create_dummy_account(name):
        """ Get a dummy testing account, using account name as a password. """
        account = AccountManager.create_account(name, name)
        return account
