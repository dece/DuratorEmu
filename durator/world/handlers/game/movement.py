from durator.config import CONFIG
from durator.world.game.movement import Movement
from durator.world.game.update_object_packet import (
    UpdateType, UpdateObjectPacket )
from durator.world.world_connection_state import WorldConnectionState


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
        player = self.conn.player
        dist_range = float(CONFIG["world"]["update_range"])
        players_guids = object_manager.players_in_range_of(player, dist_range)

        update_infos = { "unit": player }
        packet = UpdateObjectPacket(UpdateType.MOVEMENT, update_infos)
        self.conn.server.broadcast(
            packet,
            state = WorldConnectionState.IN_WORLD,
            guids = players_guids
        )
