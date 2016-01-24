from struct import Struct

from durator.common.crypto.session_cipher import SessionCipher
from durator.config import DEBUG
from durator.world.opcodes import OpCode
from pyshgck.format import dump_data
from pyshgck.logger import LOG


class WorldPacket(object):
    """ Describe a world server packet. The opcode can be None if unknown. """

    OUTGOING_SIZE_BIN   = Struct(">H")
    OUTGOING_OPCODE_BIN = Struct("<H")

    def __init__(self, opcode = None, data = b""):
        self.opcode = opcode
        self.data = data

    def to_socket(self, session_cipher = None):
        """ Return ready-to-send bytes, possibly encrypted, from the packet. """
        if DEBUG:
            print(">>>", self.opcode)
            print(dump_data(self.data), end = "")

        opcode_bytes = self.OUTGOING_OPCODE_BIN.pack(self.opcode.value)
        packet = opcode_bytes + self.data
        size_bytes = self.OUTGOING_SIZE_BIN.pack(len(packet))
        packet = size_bytes + packet

        if session_cipher is not None:
            packet = session_cipher.encrypt(packet)

        return packet


class WorldPacketReceiver(object):
    """ Helper class that can get a complete WorldPacket from a connection. """

    def __init__(self, socket):
        self.socket = socket
        self.session_cipher = None
        self.packet_buf = b""

        # This data has to be reset after each packet (see clean())
        self.packet_size = -1
        self.opcode = None
        self.content = b""

    def get_next_packet(self):
        """ Return a received WorldPacket.

        It captures when a connection get closed (recv returns None), and return
        None as well, but it doesn't capture other network exceptions like
        ConnectionResetError.
        """
        try:
            self._get_header()
            self._get_content()
        except WorldPacketReceiverException:
            return None

        if DEBUG:
            if self.opcode is not None:
                print("<<<", self.opcode)
            print(dump_data(self.content), end = "")

        packet = WorldPacket(self.opcode, self.content)
        self.clean()
        return packet

    def _get_header(self):
        """ Ensure we get all the (possibly decrypted) data from the header. """
        while len(self.packet_buf) < SessionCipher.DECRYPT_HEADER_SIZE:
            self._get_more_data()

        if self.session_cipher is not None:
            self.packet_buf = self.session_cipher.decrypt(self.packet_buf)

        self._slice_packet_size()

    def _slice_packet_size(self):
        """ Cut the packet size from packet_buf. """
        packet_size = int.from_bytes(self.packet_buf[:2], "big")
        self.packet_size = packet_size
        self.packet_buf = self.packet_buf[2:]

    def _get_content(self):
        while len(self.packet_buf) < self.packet_size:
            self._get_more_data()

        self.content = self.packet_buf[:self.packet_size]
        self.packet_buf = self.packet_buf[self.packet_size:]

        self._slice_packet_opcode()

    def _slice_packet_opcode(self):
        """ Cut the packet opcode from content. """
        opcode_bytes = self.content[:4]
        opcode_value = int.from_bytes(opcode_bytes, "little")
        self.content = self.content[4:]

        try:
            self.opcode = OpCode(opcode_value)
        except ValueError:
            LOG.warning("Unknown opcode {:X}".format(opcode_value))

    def _get_more_data(self):
        some_data = self.socket.recv(1024)
        if not some_data:
            raise WorldPacketReceiverException()
        self.packet_buf += some_data

    def clean(self):
        self.packet_size = -1
        self.opcode = None
        self.content = b""


class WorldPacketReceiverException(Exception):
    pass
