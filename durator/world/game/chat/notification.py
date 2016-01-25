from enum import Enum

from pyshgck.logger import LOG


class NotificationType(Enum):
    """ Untested values are commented. """

    # JOINED                = 0x00
    # LEFT                  = 0x01
    YOU_JOINED            = 0x02
    # YOU_LEFT              = 0x03
    WRONG_PASSWORD        = 0x04
    # NOT_MEMBER            = 0x05
    # NOT_MODERATOR         = 0x06
    # PASSWORD_CHANGED      = 0x07
    # OWNER_CHANGED         = 0x08
    # PLAYER_NOT_FOUND      = 0x09
    # NOT_OWNER             = 0x0A
    # CHANNEL_OWNER         = 0x0B
    # MODE_CHANGE           = 0x0C
    # ANNOUNCEMENTS_ON      = 0x0D
    # ANNOUNCEMENTS_OFF     = 0x0E
    # MODERATION_ON         = 0x0F
    # MODERATION_OFF        = 0x10
    # MUTED                 = 0x11
    # PLAYER_KICKED         = 0x12
    # BANNED                = 0x13
    # PLAYER_BANNED         = 0x14
    # PLAYER_UNBANNED       = 0x15
    # PLAYER_NOT_BANNED     = 0x16
    # PLAYER_ALREADY_MEMBER = 0x17
    # INVITE                = 0x18
    # INVITE_WRONG_FACTION  = 0x19
    # WRONG_FACTION         = 0x1A
    # INVALID_NAME          = 0x1B
    # NOT_MODERATED         = 0x1C
    # PLAYER_INVITED        = 0x1D
    # PLAYER_INVITE_BANNED  = 0x1E
    # THROTTLED             = 0x1F


class Notification(object):

    def __init__(self, notif_type, channel):
        self.notif_type = notif_type
        self.channel = channel

    def to_bytes(self):
        data = b""
        data += int.to_bytes(self.notif_type.value, 1, "little")
        data += self.channel.name.encode("utf8") + b"\x00"

        if self.notif_type == NotificationType.YOU_JOINED:
            chan_id = self.channel.internal_id
            data += int.to_bytes(chan_id, 4, "little")
            if chan_id == 0:
                data += b"\x00"  # Non internal channels have an additional str

        return data
