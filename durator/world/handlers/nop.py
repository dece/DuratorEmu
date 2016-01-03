
class NopHandler(object):
    """ Acknowledge but ignore that packet. """

    def __init__(self, connection, packet):
        self.conn = connection
        self.packet = packet

    def process(self):
        return None, None
