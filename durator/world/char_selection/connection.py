import os
from struct import Struct

from durator.world.char_selection.auth_session import AuthSessionHandler
from durator.world.char_selection.connection_state import CharSelectionState
from durator.world.opcodes import OpCode
from pyshgck.format import dump_data
from pyshgck.logger import LOG


class CharSelectionConnection(object):
    """ Handle a client connection during the char selection process.

    During this step, the server and the client communicate about character
    listing, character creation, etc. The server has to start the dialog with
    an auth challenge.
    """

    PACKET_SIZE_BIN    = Struct(">H")
    AUTH_CHALLENGE_BIN = Struct("<HI")

    LEGAL_OPS = {
        CharSelectionState.INIT: [ OpCode.CMSG_AUTH_SESSION ]
    }

    OP_HANDLERS = {
        OpCode.CMSG_AUTH_SESSION: AuthSessionHandler
    }

    END_STATES = [ CharSelectionState.ERROR ]

    def __init__(self, world_server, connection):
        self.world_server = world_server
        self.socket = connection
        self.state = CharSelectionState.INIT
        self.auth_seed = int.from_bytes(os.urandom(4), "little")

    def process(self):
        LOG.debug("Entering the char selection process")
        self._send_auth_challenge()
        while self.state not in CharSelectionConnection.END_STATES:
            data = self._recv_packet()
            print(dump_data(data), end = "")
            self._handle_packet(data)

            if self.state in CharSelectionConnection.END_STATES:
                break

    def _send_packet(self, data):
        """ Send data prepended with the data size in big endian. """
        packet = CharSelectionConnection.PACKET_SIZE_BIN.pack(len(data)) + data
        self.socket.sendall(packet)

    def _recv_packet(self):
        """ Receive a full-sized packet, and return it without the size uint16.

        Ok so if two packets get packed in the same TCP frame, we might get them
        concatenated, right? The fact that the data size prepended is of various
        size and endianness sucks, but if I find some consistency later I might
        write a generic packet handler that'll handle all that.
        """
        data = b""
        while True:
            data_part = self.socket.recv(1024)
            if not data:
                return None
            data += data_part

            if len(data) < 2:
                continue

            packet_size = int.from_bytes(data[0:2], "big")
            if len(data[2:]) >= packet_size:
                return data[2 : 2+packet_size]

    def _handle_packet(self, packet):
        opcode_value = int.from_bytes(packet[0:2], "little")
        opcode = OpCode(opcode_value)
        if not self.is_opcode_legal(opcode):
            LOG.error( "Char selection: Received opcode " + str(opcode) +
                       " in state " + str(self.state) )
            self.state = CharSelectionState.ERROR
            return

        handler_class = CharSelectionConnection.OP_HANDLERS.get(opcode)
        self._call_handler(handler_class, packet)

    def _call_handler(self, handler_class, packet):
        handler = handler_class(self, packet)
        next_state, response = handler.process()

        if response:
            self.socket.sendall(response)

        if next_state is not None:
            self.state = next_state

    def is_opcode_legal(self, opcode):
        """ Check if that opcode is legal for the current connection state. """
        return opcode in CharSelectionConnection.LEGAL_OPS[self.state]

    def _send_auth_challenge(self):
        packet = CharSelectionConnection.AUTH_CHALLENGE_BIN.pack(
            OpCode.SMSG_AUTH_CHALLENGE.value,
            self.auth_seed
        )
        self._send_packet(packet)
