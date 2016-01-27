""" {C,S}MSG_MESSAGECHAT structures """

from enum import Enum
import io
from struct import Struct

from durator.world.game.chat.language import Language
from durator.world.opcodes import OpCode
from durator.world.world_packet import WorldPacket
from pyshgck.bin import read_cstring, read_struct


class ChatMessageType(Enum):

    SAY                    = 0x00
    PARTY                  = 0x01
    RAID                   = 0x02
    GUILD                  = 0x03
    OFFICER                = 0x04
    YELL                   = 0x05
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


class ChatMessageTag(Enum):

    NONE = 0
    AFK  = 1
    DND  = 2
    GM   = 3


class ClientChatMessage(object):

    # - uint32    type
    # - uint32    language
    #     if type == CHANNEL
    #     - string    name?
    #     endif
    # - string    message (size above)

    HEADER_BIN = Struct("<2I")

    def __init__(self):
        self.message_type = None
        self.language = None
        self.channel_name = ""
        self.content = ""

    @staticmethod
    def from_client(data):
        message = ClientChatMessage()
        data_io = io.BytesIO(data)

        header_data = read_struct(data_io, ClientChatMessage.HEADER_BIN)
        message.message_type = ChatMessageType(header_data[0])
        message.language = Language(header_data[1])

        if message.message_type == ChatMessageType.CHANNEL:
            channel_name = read_cstring(data_io, data_io.tell())
            message.channel_name = channel_name.decode("utf8")

        content = read_cstring(data_io, data_io.tell())
        message.content = content.decode("utf8")

        return message


class ServerChatMessage(object):

    # From the client SMSG_MESSAGECHAT handler, discarding some flags.
    # - uint8     type
    # - uint32    language
    #     if type == CHANNEL
    #     - string    name?
    #     endif
    # - uint64    guid
    # - uint32    size
    # - string    message (size above)
    # - uint8     tag

    HEADER_BIN      = Struct("<BI")
    MIDDLE_PART_BIN = Struct("<QI")

    def __init__(self):
        self.message_type = None
        self.language = None
        self.channel_name = ""
        self.content = ""

        self.sender_guid = 0
        self.content_size = 0
        self.tag = ChatMessageTag.NONE

    def load_client_message(self, client_message):
        self.message_type = client_message.message_type
        self.language = client_message.language
        self.channel_name = client_message.channel_name
        self.content = client_message.content

    def to_bytes(self):
        data = b""
        data += self.HEADER_BIN.pack(
            self.message_type.value,
            self.language.value
        )

        if self.message_type == ChatMessageType.CHANNEL:
            data += self.channel_name.encode("utf8") + b"\x00"

        content_bytes = self.content.encode("utf8") + b"\x00"
        self.content_size = len(content_bytes)

        data += self.MIDDLE_PART_BIN.pack(
            self.sender_guid,
            self.content_size
        )
        data += content_bytes
        data += int.to_bytes(self.tag.value, 1, "little")

        return data

    def to_packet(self):
        return WorldPacket(OpCode.SMSG_MESSAGECHAT, self.to_bytes())
