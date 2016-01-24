import base64

from peewee import Model, CharField, ForeignKeyField

from durator.common.account.account import Account, AccountManager
from durator.db.database import DB, db_connection
from pyshgck.logger import LOG


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
    def delete_session(account):
        """ Delete the session assiociated with that account. """
        try:
            session = AccountSession.get(AccountSession.account == account)
            session.delete_instance()
        except AccountSession.DoesNotExist:
            LOG.warning("Tried to delete an non-existing session.")

    @staticmethod
    @db_connection
    def delete_all_sessions():
        """ Delete all account sessions to clean up the database. """
        AccountSession.delete().execute()
