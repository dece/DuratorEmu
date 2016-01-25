from durator.world.game.chat.notification import Notification, NotificationType


class LeaveChannelHandler(object):

    def __init__(self, connection, packet):
        self.conn = connection
        self.packet = packet

        self.channel_name = ""

    def process(self):
        self._parse_packet(self.packet)

        leave_result_code = self._try_leave_channel()
        response_packet = self._get_response_packet(leave_result_code)
        return None, response_packet

    def _parse_packet(self, packet):
        self.channel_name = packet[:-1].decode("utf8")

    def _try_leave_channel(self):
        leave_result_code = self.conn.server.chat_manager.leave_channel(
            self.conn.player, self.channel_name
        )
        return leave_result_code

    def _get_response_packet(self, leave_result_code):
        notif_type = {
            0: NotificationType.YOU_LEFT,
            1: NotificationType.NOT_MEMBER,
            2: NotificationType.INVALID_NAME
        }[leave_result_code]

        channel = self.conn.server.chat_manager.get_channel(self.channel_name)

        notification = Notification(notif_type, channel)
        return notification.to_packet()
