from struct import Struct

from durator.world.game.chat.message import ClientChatMessage


class MessageHandler(object):
    """ Handle basic CMSG_MESSAGECHAT packets. """

    PACKET_PART1_BIN  = Struct("<2I")

    def __init__(self, connection, packet):
        self.conn = connection
        self.packet = packet

        self.message = None

    def process(self):
        self._parse_packet(self.packet)

        player_guid = self.conn.player.guid
        chat_manager = self.conn.server.chat_manager
        chat_manager.receive_message(player_guid, self.message)

        return None, None

    def _parse_packet(self, packet):
        self.message = ClientChatMessage.from_client(packet)
