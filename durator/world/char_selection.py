


class CharSelectionProcess(object):
    """ Handle a client connection during the char selection process. """

    def __init__(self, world_server, connection):
        self.world_server = world_server
        self.socket = connection
