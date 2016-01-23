from enum import Enum


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
