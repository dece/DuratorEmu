from abc import ABCMeta, abstractmethod

from pyshgck.logger import LOG


class ConnectionAutomaton(metaclass = ABCMeta):
    """ This base class handle an active connection, handle incoming & outgoing
    packets, change state in consequence.

    The LEGAL_OPS dict takes a state as key and a list of possible opcodes. The
    OP_HANDLERS dict takes opcodes and a handler class. END_STATES is a list of
    states that means this automaton can stop.
    """

    LEGAL_OPS   = {}
    OP_HANDLERS = {}

    INIT_STATE       = None
    END_STATES       = []
    MAIN_ERROR_STATE = None

    def __init__(self, connection):
        self.socket = connection
        self.state = self.INIT_STATE

    def handle_connection(self):
        """ Call this method to let the automaton handle the connection. """
        self._actions_before_main_loop()
        while self.state not in self.END_STATES:
            packet = self._recv_packet()
            if packet is None:
                LOG.debug("Client closed the connection.")
                break

            self._try_handle_packet(packet)
            self._actions_after_handle_packet()

    @abstractmethod
    def _send_packet(self, data):
        """ Prepend necessary infos to data and send it through the socket.
        Data has the format returned by the packet handlers' response. """
        pass

    @abstractmethod
    def _recv_packet(self):
        """ Receive a message from the socket and return the packet or None. """
        pass

    def _try_handle_packet(self, packet):
        try:
            self._handle_packet(packet)
        except Exception as exc:
            LOG.error("Uncaught exception in {}.{}: {}".format(
                type(self).__name__, "_try_handle_packet", str(exc)
            ))
            raise

    def _handle_packet(self, packet):
        opcode, packet_data = self._parse_packet(packet)
        if opcode is None:
            LOG.warning("{}: unknown opcode, ignoring packet.".format(
                type(self).__name__
            ))
            return

        if not self.opcode_is_legal(opcode):
            LOG.error("{}: received illegal opcode {} in state {}".format(
                type(self).__name__, str(opcode), str(self.state)
            ))
            self.state = self.MAIN_ERROR_STATE
            return

        handler_class = self.OP_HANDLERS.get(opcode)
        if handler_class is None:
            LOG.warning("{}: known opcode without handler: {}".format(
                type(self).__name__, str(opcode)
            ))
            self.state = self.MAIN_ERROR_STATE
            return

        self._call_handler(handler_class, packet_data)

    @abstractmethod
    def _parse_packet(self, packet):
        """ Return opcode and packet content. Packet has the format returned by
        the _recv_packet method. """
        pass

    def _call_handler(self, handler_class, packet_data):
        handler = handler_class(self, packet_data)
        next_state, response = handler.process()

        if response:
            self._send_packet(response)
        if next_state is not None:
            self.state = next_state

    def opcode_is_legal(self, opcode):
        """ Check if that opcode is legal for the current connection state. """
        return opcode in self.LEGAL_OPS[self.state]

    def _actions_before_main_loop(self):
        """ Perform possible required actions before looping over packets. """
        pass

    def _actions_after_handle_packet(self):
        """ Perform possible required actions after packet handling. """
        pass
