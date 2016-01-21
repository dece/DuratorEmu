from enum import Enum


class AccountDataType(Enum):

    GLOBAL_CONFIG      = 0
    CHARACTER_CONFIG   = 1
    GLOBAL_BINDINGS    = 2
    CHARACTER_BINDINGS = 3
    GLOBAL_MACROS      = 4

    @property
    def flag(self):
        return 1 << self.value

    @staticmethod
    def from_index(index):
        return AccountDataType(1 << index)


class AccountDataTypeMask(Enum):

    GLOBAL = (
        AccountDataType.GLOBAL_CONFIG.flag   |
        AccountDataType.GLOBAL_BINDINGS.flag |
        AccountDataType.GLOBAL_MACROS.flag
    )
    CHARACTER = (
        AccountDataType.CHARACTER_CONFIG.flag   |
        AccountDataType.CHARACTER_BINDINGS.flag
    )


NUM_ACCOUNT_DATA_TYPES = len(AccountDataType)


class AccountData(object):

    def __init__(self, caches = None):
        self.caches = caches
        if self.caches is None:
            self._init_dummy_caches()

    def _init_dummy_caches(self):
        self.caches = [None] * NUM_ACCOUNT_DATA_TYPES
        for index in range(NUM_ACCOUNT_DATA_TYPES):
            self.caches[index] = AccountDataCache()

    def get_cache(self, data_type):
        return self.caches[data_type.value]

    def get_times(self, mask):
        times = []
        for data_type in list(AccountDataType):
            if data_type.flag & mask.value:
                cache = self.get_cache(data_type)
                times.append(cache.time)
        return times


class AccountDataCache(object):

    def __init__(self, time = 0, data = ""):
        self.time = time
        self.data = data
