from durator.world.opcodes import OpCode
from pyshgck.format import dump_data


class WorldPacket(object):

    _PACKET_BUF = b""

    def __init__(self):
        self.length = 0
        self.opcode = None
        self.data = b""

    @staticmethod
    def from_socket(socket):
        """ Receive a WorldPacket through socket, or None if the connection is
        closed during reception. """
        packet = WorldPacket()
        while True:
            # Receive data as long as the connection is opened.
            data_part = socket.recv(1024)
            if not data_part:
                return None
            WorldPacket._PACKET_BUF += data_part

            # If there isn't enough to compute the packet size, just continue
            # receiving data.
            if len(WorldPacket._PACKET_BUF) < 2:
                continue

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

        print(dump_data(data), end = "")
        packet.length = packet_size
        opcode_bytes, data = data[0:4], data[4:]
        opcode_value = int.from_bytes(opcode_bytes, "little")
        packet.opcode = OpCode(opcode_value)
        packet.data = data
        return packet
