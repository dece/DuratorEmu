from durator.world.game.movement import Movement


class MovementHandler(object):
    """ Handle all player movement opcodes. """

    def __init__(self, connection, packet):
        self.conn = connection
        self.packet = packet

        self.movement = None

    def process(self):
        self.movement = Movement.from_bytes(self.packet)
        self._update_position()
        return None, None

    def _update_position(self):
        """ Update player position according to the received Movement.

        This currently doesn't take into account transports and stuff, it just
        update the player position from the base position in the Movement.
        """
        self.conn.player.position = self.movement.position
