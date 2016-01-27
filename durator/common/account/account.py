import base64
from enum import Enum
import re

from peewee import Model, CharField, IntegerField

from durator.db.database import DB


ACCOUNT_NAME_RE = re.compile(r"\w+")


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
