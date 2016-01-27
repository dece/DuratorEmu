""" Handlers for CMSG_REQUEST_ACCOUNT_DATA and CMSG_UPDATE_ACCOUNT_DATA. """

from struct import Struct

from durator.common.account.account_data import AccountDataType
from durator.common.account.managers import AccountDataManager


class RequestAccountDataHandler(object):

    def __init__(self, connection, packet):
        self.conn = connection
        self.packet = packet

    def process(self):
        return None, None


class UpdateAccountDataHandler(object):

    HEADER_BIN = Struct("<2I")

    def __init__(self, connection, packet):
        self.conn = connection
        self.packet = packet

        self.data_type = None
        self.decompressed_size = 0
        self.zlib_data = b""

    def process(self):
        self._parse_packet(self.packet)
        self._update_account_data()
        return None, None

    def _parse_packet(self, packet):
        header_size = self.HEADER_BIN.size
        header, content = packet[:header_size], packet[header_size:]
        data_type_value, decomp_size = self.HEADER_BIN.unpack(header)

        self.data_type = AccountDataType(data_type_value)
        self.decompressed_size = decomp_size
        self.zlib_data = content

    def _update_account_data(self):
        AccountDataManager.set_account_data(
            self.conn.account, self.data_type, self.zlib_data
        )
