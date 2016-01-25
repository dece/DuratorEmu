from enum import Enum
import io
from struct import Struct

from durator.world.game.chat.language import Language
from pyshgck.bin import read_cstring, read_struct


class ChatMessageType(Enum):

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

    # From the client SMSG_MESSAGECHAT handler, discarding some flags.
    # Note that the CMSG is much simpler.
    # - uint8     type
    # - uint32    language
    #     if type == CHANNEL
    #     - string    name?
    #     endif
    # - uint64    guid
    # - uint32    size
    # - string    message (size above)
    # - uint8     tag

    HEADER_BIN = Struct("<2I")

    def __init__(self):
        self.message_type = None
        self.language = 0
        self.channel_name = ""
        self.content = ""

        self.guid = 0
        self.content_size = 0
        self.tag = None

    @staticmethod
    def from_client(data):
        message = ChatMessage()
        data_io = io.BytesIO(data)

        header_data = read_struct(data_io, ChatMessage.HEADER_BIN)
        message.message_type = ChatMessageType(header_data[0])
        message.language = Language(header_data[1])

        if message.message_type == ChatMessageType.CHANNEL:
            message.channel_name = read_cstring(data_io, data_io.tell())

        message.content = read_cstring(data_io, data_io.tell())

        return message
