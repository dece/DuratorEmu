from struct import Struct

from durator.world.game.object_manager import OBJECT_MANAGER
from durator.world.opcodes import OpCode
from durator.world.world_connection_state import WorldConnectionState
from durator.world.world_packet import WorldPacket


class LogoutRequestHandler(object):
    """ Handle client logout request. Do not respect the retail logout timer,
    just throw him away. """

    LOGOUT_RESPONSE_BIN = Struct("<IB")
    LOGOUT_COMPLETE_BIN = Struct("<")

    def __init__(self, connection, packet):
        self.conn = connection
        self.packet = packet

    def process(self):
        if self.can_logout():
            self.conn.send_packet(self._get_logout_response_packet(True))
            self.conn.send_packet(self._get_logout_complete_packet())
            self.conn.unset_player()
            return WorldConnectionState.AUTH_OK, None
        else:
            self.conn.send_packet(self._get_logout_response_packet(False))
            return None, None

    def can_logout(self):
        return not self.conn.player.is_falling()

    def _get_logout_response_packet(self, can_logout):
        response_value = 0 if can_logout else 1
        response_data = self.LOGOUT_RESPONSE_BIN.pack(response_value, 0)
        return WorldPacket(OpCode.SMSG_LOGOUT_RESPONSE, response_data)

    def _get_logout_complete_packet(self):
        return WorldPacket(OpCode.SMSG_LOGOUT_COMPLETE)
