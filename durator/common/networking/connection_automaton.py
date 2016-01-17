from abc import ABCMeta, abstractmethod
import traceback

from pyshgck.logger import LOG


class ConnectionAutomaton(metaclass = ABCMeta):
    """ This base class handles an active connection, handles incoming and
    outgoing packets, change state in consequence. Some opcodes are considered
    legal only if the automaton is in a determined state, to ensure protocol
    integrity.

    * The LEGAL_OPS dict takes a state as key and a list of possible opcodes.
    * UNMANAGED_OPS is a list of opcodes that do not require a special state.
    * The OP_HANDLERS dict takes opcodes and a handler class.
    * INIT_STATE is the entry state of the automaton
    * END_STATES is a list of states that means this automaton can stop.
    * MAIN_ERROR_STATE is a general end state when something went wrong.
    """

    LEGAL_OPS     = {}
    UNMANAGED_OPS = []
    OP_HANDLERS   = {}

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
        self._actions_after_main_loop()

    @abstractmethod
    def send_packet(self, data):
        """ Prepend necessary infos to data and send it through the socket.
        Data has the format returned by the packet handlers' response. """
        pass

    @abstractmethod
    def _recv_packet(self):
        """ Receive a message from the socket and return the packet or None.
        It can be a bytes object, some class or whatever, as long as the other
        parts of the class take the typ into account. """
        pass

    def _try_handle_packet(self, packet):
        try:
            self._handle_packet(packet)
        except Exception as exc:
            LOG.error("{}: uncaught exception in packet handler:".format(
                type(self).__name__
            ))
            LOG.error(str(exc))
            traceback.print_tb(exc.__traceback__)
            self.state = self.MAIN_ERROR_STATE

    def _handle_packet(self, packet):
        """ Find and call a handler for that packet.

        It is possible that we do not know the opcode, which is not a problem.
        However, if it is known, it has to be legal (in a valid state) and we
        need to enforce a handler to it, even if it's just NopHandler. If I
        don't feel like adding the simplest handler for an opcode, it probably
        shouldn't be in the OpCode enum in the first place.
        """
        opcode, packet_data = self._parse_packet(packet)
        if opcode is None:
            return

        if ( opcode not in self.UNMANAGED_OPS
             and not self.opcode_is_legal(opcode) ):
            LOG.error("{}: received illegal opcode {} in state {}".format(
                type(self).__name__, str(opcode), str(self.state)
            ))
            self.state = self.MAIN_ERROR_STATE
            return

        handler_class = self.OP_HANDLERS.get(opcode)
        if handler_class is None:
            LOG.error("{}: known opcode without handler: {}".format(
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
        """ Call the handler and possibly send a response packet and update
        the connection state. """
        handler = handler_class(self, packet_data)
        next_state, response = handler.process()

        if response:
            self.send_packet(response)
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

    def _actions_after_main_loop(self):
        """ Perform possible required actions after looping over packets. """
        pass
