from durator.world.game.movement import Movement


class MovementHandler(object):
    """ Handle all player movement opcodes. """

    def __init__(self, connection, packet):
        self.conn = connection
        self.packet = packet

        self.movement = None

    def process(self):
        self.movement = Movement.from_bytes(self.packet)
        return None, None
