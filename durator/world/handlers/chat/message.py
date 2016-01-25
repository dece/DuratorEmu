import io
from struct import Struct

from durator.world.game.chat.message import ChatMessage
from durator.world.opcodes import OpCode
from durator.world.world_packet import WorldPacket


class MessageHandler(object):
    """ Handle basic CMSG_MESSAGECHAT packets. """

    PACKET_PART1_BIN  = Struct("<2I")

    def __init__(self, connection, packet):
        self.conn = connection
        self.packet = packet

        self.message = None

    def process(self):
        self._parse_packet(self.packet)
        self.conn.server.chat_manager.receive_chat_message(ChatMessage)
        return None, None

    def _parse_packet(self, packet):
        self.message = ChatMessage.from_client(packet)
