import base64
from enum import Enum
import re

from peewee import Model, CharField, IntegerField, ForeignKeyField

from durator.auth.srp import Srp
from durator.db.database import DB, db_connection


_ACCOUNT_NAME_RE = re.compile(r"\w+")


class AccountStatus(Enum):
    """ Determine if an account can log in (VALID) or not (any other value). """

    NOT_READY = 0
    VALID     = 1
    BANNED    = 2
    SUSPENDED = 3


class Account(Model):
    """ Account with SRP data.

    Attributes:
        name: account name
        status: AccountStatus, determine if that account is usable or not
        srp_salt: 32-byte SRP salt, stored as base64
        srp_verifier: big int, stored as base64'd little endian bytes
    """

    name         = CharField(max_length = 64)
    status       = IntegerField(default = AccountStatus.NOT_READY.value)
    srp_salt     = CharField(max_length = 64)
    srp_verifier = CharField(max_length = 64)

    class Meta(object):
        database = DB

    def is_valid(self):
        return self.status == AccountStatus.VALID.value

    @property
    def srp_salt_as_bytes(self):
        return base64.b64decode(self.srp_salt.encode("ascii"))
    @srp_salt_as_bytes.setter
    def srp_salt_as_bytes(self, value_bytes):
        self.srp_salt = base64.b64encode(value_bytes).decode("ascii")

    @property
    def srp_verifier_as_int(self):
        verifier_bytes = base64.b64decode(self.srp_verifier.encode("ascii"))
        return int.from_bytes(verifier_bytes, "little")
    @srp_verifier_as_int.setter
    def srp_verifier_as_int(self, value_int):
        verifier_bytes = int.to_bytes(value_int, 32, "little")
        self.srp_verifier = base64.b64encode(verifier_bytes).decode("ascii")


class AccountSession(Model):

    account     = ForeignKeyField(Account, unique = True)
    session_key = CharField(max_length = 80)

    class Meta(object):
        database = DB

    @property
    def session_key_as_bytes(self):
        return base64.b64decode(self.session_key.encode("ascii"))
    @session_key_as_bytes.setter
    def session_key_as_bytes(self, value_bytes):
        self.session_key = base64.b64encode(value_bytes).decode("ascii")


class AccountManager(object):
    """ Collection of functions to manage the accounts in the database. """

    @staticmethod
    @db_connection
    def create_account(account_name, password):
        """ Create a valid account and add it to the database, or None if the
        arguments are invalid. """
        if not _ACCOUNT_NAME_RE.match(account_name):
            return None

        account = Account( name = account_name.upper()
                         , status = AccountStatus.NOT_READY.value )
        Srp.generate_account_srp_data(account, password)
        account.status = AccountStatus.VALID.value
        account.save()
        return account

    @staticmethod
    def create_dummy_account(name):
        """ Get a dummy testing account, using account name as a password. """
        account = AccountManager.create_account(name, name)
        return account

    @staticmethod
    @db_connection
    def get_account(account_name):
        """ Return the account from the database if it exists, or None. """
        try:
            return Account.get(Account.name == account_name)
        except Account.DoesNotExist:
            return None


class AccountSessionManager(object):
    """ Collection of functions to manage the sessions in the database. """

    @staticmethod
    @db_connection
    def add_session(account, session_key):
        """ Add a new session for that account, or update the session_key if the
        account already had a session. """
        session = AccountSessionManager.get_session(account.name)
        if session is None:
            session = AccountSession(account = account)
        session.session_key_as_bytes = session_key
        session.save()

    @staticmethod
    @db_connection
    def get_session(account_name):
        """ Return the session associated with the account with that name,
        or None if no session or account can be found. """
        account = AccountManager.get_account(account_name)
        if account is None:
            return None

        try:
            return AccountSession.get(AccountSession.account == account)
        except AccountSession.DoesNotExist:
            return None

    @staticmethod
    @db_connection
    def delete_all_sessions():
        AccountSession.delete().execute()
