import base64

from peewee import Model, CharField, ForeignKeyField

from durator.common.account.account import Account
from durator.db.database import DB


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
