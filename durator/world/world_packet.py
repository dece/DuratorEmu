from durator.world.opcodes import OpCode
from pyshgck.format import dump_data


_PACKET_BUFFER = b""


class WorldPacket(object):

    def __init__(self):
        self.length = 0
        self.opcode = None
        self.data = b""

    @staticmethod
    def from_socket(socket):
        """ Receive a WorldPacket through socket, or None if the connection is
        closed during reception. """
        global _PACKET_BUFFER

        packet = WorldPacket()
        while True:
            # Receive data as long as the connection is opened.
            data_part = socket.recv(1024)
            if not data_part:
                return None
            _PACKET_BUFFER += data_part

            # If there isn't enough to compute the packet size, just continue
            # receiving data.
            if len(_PACKET_BUFFER) < 2:
                continue

            packet_size = int.from_bytes(_PACKET_BUFFER[0:2], "big")

            # Now that we have a packet size, wait until we have all the data
            # of this packet.
            if len(_PACKET_BUFFER[2:]) < packet_size:
                continue

            # When all the packet is in the static buffer, cut it from the
            # buffer and return it.
            _PACKET_BUFFER = _PACKET_BUFFER[2:]
            data = _PACKET_BUFFER[:packet_size]
            _PACKET_BUFFER = _PACKET_BUFFER[packet_size:]
            break

        print(dump_data(data), end = "")
        packet.length = packet_size
        opcode_bytes, data = data[0:4], data[4:]
        opcode_value = int.from_bytes(opcode_bytes, "little")
        packet.opcode = OpCode(opcode_value)
        packet.data = data
        return packet
