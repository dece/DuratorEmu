import binascii
from enum import Enum
import zlib

from peewee import Model, CharField, ForeignKeyField, IntegerField, TextField

from durator.common.account.account import Account
from durator.common.crypto.md5 import md5
from durator.db.database import DB, db_connection


class AccountDataType(Enum):

    CONFIG   = 0
    BINDINGS = 1
    MACROS   = 2
    LAYOUT   = 3
    CHAT     = 4

    def as_flag(self):
        return 1 << self.value

    @staticmethod
    def full_mask():
        return sum([data_type.as_flag() for data_type in AccountDataType])


NUM_ACCOUNT_DATA_TYPES = len(AccountDataType)


class AccountData(Model):

    account           = ForeignKeyField(Account)
    data_type         = IntegerField()
    decompressed_size = IntegerField()
    content           = TextField()
    md5               = CharField(max_length = 16*2)

    class Meta(object):
        database = DB

    @property
    def content_as_zlib_data(self):
        return zlib.compress(self.content.encode("utf8"))
    @content_as_zlib_data.setter
    def content_as_zlib_data(self, value_bytes):
        try:
            self.content = zlib.decompress(value_bytes).decode("utf8")
        except zlib.error:
            self.content = ""

    @property
    def md5_as_bytes(self):
        return binascii.a2b_hex(self.md5.encode("ascii"))
    @md5_as_bytes.setter
    def md5_as_bytes(self, value_bytes):
        self.md5 = binascii.b2a_hex(value_bytes).decode("ascii")





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
    @db_connection
    def set_account_data(account, data_type, compressed_data):
        """ Update values for that account and data_type with this data. """
        account_data = AccountDataManager.get_account_data(account, data_type)

        account_data.content_as_zlib_data = compressed_data
        account_data.decompressed_size = len(account_data.content)

        content_bytes = account_data.content.encode("utf8", errors = "replace")
        account_data.md5_as_bytes = md5(content_bytes)

        account_data.save()
