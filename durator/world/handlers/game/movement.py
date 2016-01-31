from durator.world.game.movement import Movement


class MovementHandler(object):
    """ Handle all player movement opcodes. """

    def __init__(self, connection, packet):
        self.conn = connection
        self.packet = packet

        self.movement = None

    def process(self):
        self.movement = Movement.from_bytes(self.packet)
        self._update_player()
        self._notify_near_players()
        return None, None

    def _update_player(self):
        """ Update player data according to the received Movement.

        This currently doesn't take into account transports and stuff, it just
        update the player position from the base position in the Movement.
        """
        player = self.conn.player
        with player.lock:
            player.movement = self.movement
            player.position = self.movement.position

    def _notify_near_players(self):
        object_manager = self.conn.server.object_manager
        object_manager.update_movement(self.conn.player)
