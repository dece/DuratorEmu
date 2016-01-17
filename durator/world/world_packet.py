from struct import Struct

from durator.common.crypto.session_cipher import SessionCipher
from durator.config import DEBUG
from durator.world.opcodes import OpCode
from pyshgck.format import dump_data
from pyshgck.logger import LOG


class WorldPacket(object):

    OUTGOING_SIZE_BIN   = Struct(">H")
    OUTGOING_OPCODE_BIN = Struct("<H")

    # This static packet buffer ensures that all world packets are correctly
    # received in their entirety.
    _PACKET_BUF = b""

    def __init__(self, data = None):
        self.opcode = None
        self.data = data or b""

    @staticmethod
    def from_socket(socket, session_cipher = None):
        """ Receive a WorldPacket through socket, or None if the connection is
        closed during reception. """
        packet = WorldPacket()
        while True:
            # Receive data as long as the connection is opened.
            data_part = socket.recv(1024)
            if not data_part:
                return None
            WorldPacket._PACKET_BUF += data_part

            # Continue receiving data until we have a complete header.
            if len(WorldPacket._PACKET_BUF) < SessionCipher.DECRYPT_HEADER_SIZE:
                continue

            # If a session cipher is provided, use it to decrypt the header.
            if session_cipher is not None:
                decrypted = session_cipher.decrypt(WorldPacket._PACKET_BUF)
                WorldPacket._PACKET_BUF = decrypted

            packet_size = int.from_bytes(WorldPacket._PACKET_BUF[0:2], "big")
            WorldPacket._PACKET_BUF = WorldPacket._PACKET_BUF[2:]

            # Now that we have a packet size, wait until we have all the data
            # of this packet.
            if len(WorldPacket._PACKET_BUF) < packet_size:
                continue

            # When all the packet is in the static buffer, cut it from the
            # buffer and return it.
            data = WorldPacket._PACKET_BUF[:packet_size]
            WorldPacket._PACKET_BUF = WorldPacket._PACKET_BUF[packet_size:]
            break

        if DEBUG:
            print("<<<")
            print(dump_data(data), end = "")

        opcode_bytes, data = data[:4], data[4:]
        opcode_value = int.from_bytes(opcode_bytes, "little")
        try:
            packet.opcode = OpCode(opcode_value)
        except ValueError:
            LOG.warning("Unknown opcode {:X}".format(opcode_value))
        packet.data = data
        return packet

    def to_socket(self, session_cipher = None):
        """ Return ready-to-send bytes, possibly encrypted, from the packet. """
        opcode_bytes = self.OUTGOING_OPCODE_BIN.pack(self.opcode.value)
        packet = opcode_bytes + self.data
        size_bytes = self.OUTGOING_SIZE_BIN.pack(len(packet))
        packet = size_bytes + packet

        if session_cipher is not None:
            packet = session_cipher.encrypt(packet)

        return packet
