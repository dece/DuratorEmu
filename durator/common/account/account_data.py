import binascii
from enum import Enum
import zlib

from peewee import Model, CharField, ForeignKeyField, IntegerField, TextField

from durator.common.account.account import Account
from durator.db.database import DB


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
