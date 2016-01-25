from enum import Enum


class MessageType(Enum):

    SAY                    = 0x00  # ok
    PARTY                  = 0x01
    RAID                   = 0x02
    GUILD                  = 0x03  # ok
    OFFICER                = 0x04
    YELL                   = 0x05  # ok
    WHISPER                = 0x06
    WHISPER_INFORM         = 0x07
    EMOTE                  = 0x08
    TEXT_EMOTE             = 0x09

    SYSTEM                 = 0x0A

    MONSTER_SAY            = 0x0B
    MONSTER_YELL           = 0x0C
    MONSTER_EMOTE          = 0x0D
    MONSTER_WHISPER        = 0x1A

    CHANNEL                = 0x0E
    CHANNEL_JOIN           = 0x0F
    CHANNEL_LEAVE          = 0x10
    CHANNEL_LIST           = 0x11
    CHANNEL_NOTICE         = 0x12
    CHANNEL_NOTICE_USER    = 0x13

    AFK                    = 0x14
    DND                    = 0x15
    IGNORED                = 0x16

    SKILL                  = 0x17
    LOOT                   = 0x18


class MessageTag(Enum):

    NONE = 0
    AFK  = 1
    DND  = 2
    GM   = 3


class ChatMessage(object):

    # From the client SMSG_MESSAGECHAT handler, discarding some flags
    # uint8     type
    # uint32    flags?
    #   if type == CHANNEL
    #     string    name?
    #   endif
    # uint64    guid
    # uint32    size
    # string    message (size above)
    # uint8     tag

    def __init__(self):
        self.message_type = None
        self.flags = 0
        self.channel_name = ""
        self.guid = 0
        self.size = 0
        self.content = ""
        self.tag = None
