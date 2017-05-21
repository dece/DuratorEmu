import io
from struct import Struct

from durator.world.game.chat.notification import Notification, NotificationType
from pyshgck.bin import read_cstring


class JoinChannelHandler(object):

    PACKET_PART1_BIN  = Struct("<2I")

    def __init__(self, connection, packet):
        self.conn = connection
        self.packet = packet

        self.channel_name = ""
        self.password = ""

    def process(self):
        self._parse_packet(self.packet)

        join_result_code = self._try_join_channel()
        response_packet = self._get_response_packet(join_result_code)
        return None, response_packet

    def _parse_packet(self, packet):
        packet_io = io.BytesIO(packet)
        channel_name_bytes = read_cstring(packet_io)
        password_bytes = read_cstring(packet_io)

        self.channel_name = channel_name_bytes.decode("utf8")
        self.password = password_bytes.decode("utf8")

    def _try_join_channel(self):
        join_result_code = self.conn.server.chat_manager.join_channel(
            self.conn.player, self.channel_name, self.password
        )
        return join_result_code

    def _get_response_packet(self, join_result_code):
        notif_type = {
            0: NotificationType.YOU_JOINED,
            1: NotificationType.WRONG_PASSWORD
        }[join_result_code]

        channel = self.conn.server.chat_manager.get_channel(self.channel_name)

        notification = Notification(notif_type, channel)
        return notification.to_packet()
