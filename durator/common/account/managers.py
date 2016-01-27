from durator.auth.srp import Srp
from durator.common.account.account import (
    Account, AccountStatus, ACCOUNT_NAME_RE )
from durator.common.account.account_data import AccountData, AccountDataType
from durator.common.account.account_session import AccountSession
from durator.common.crypto.md5 import md5
from durator.db.database import db_connection
from pyshgck.logger import LOG


class AccountManager(object):
    """ Collection of functions to manage the accounts in the database. """

    @staticmethod
    @db_connection
    def create_account(account_name, password):
        """ Create a valid account and add it to the database, or None if the
        arguments are invalid. """
        if not ACCOUNT_NAME_RE.match(account_name):
            LOG.debug("Invalid account name.")
            return None

        account = Account( name = account_name.upper()
                         , status = AccountStatus.NOT_READY.value )
        Srp.generate_account_srp_data(account, password)
        account.status = AccountStatus.VALID.value
        account.save()

        AccountDataManager.create_account_data(account)

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
            LOG.warning("No account with that name: " + account_name)
            return None


class AccountDataManager(object):

    @staticmethod
    @db_connection
    def create_account_data(account):
        for data_type in AccountDataType:
            AccountData.create(
                account = account,
                data_type = data_type.value,
                decompressed_size = 0,
                content = "",
                md5 = "00"*16
            )

    @staticmethod
    @db_connection
    def get_account_data(account, data_type):
        """ Return the AccountData for that account and data_type. """
        return ( AccountData
                 .get( AccountData.account == account
                     , AccountData.data_type == data_type.value ) )

    @staticmethod
    @db_connection
    def get_account_data_md5(account):
        """ Return an ordered list of account data MD5s. """
        account_data_md5s = ( AccountData
                              .select(AccountData.md5)
                              .where(AccountData.account == account)
                              .order_by(AccountData.data_type) )
        md5s = [ad.md5_as_bytes for ad in account_data_md5s]
        return md5s

    @staticmethod
    def set_account_data(account, data_type, compressed_data):
        """ Update values for that account and data_type with this data. """
        account_data = AccountDataManager.get_account_data(account, data_type)

        account_data.content_as_zlib_data = compressed_data
        account_data.decompressed_size = len(account_data.content)

        content_bytes = account_data.content.encode("utf8", errors = "replace")
        account_data.md5_as_bytes = md5(content_bytes)

        account_data.save()


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
