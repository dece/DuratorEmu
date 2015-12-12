from pyshgck.logger import LOG


class CharSelectionProcess(object):
    """ Handle a client connection during the char selection process.

    During this step, the server and the client communicate about character
    listing, character creation, etc. The server has to start the dialog with
    an auth challenge.
    """

    def __init__(self, world_server, connection):
        self.world_server = world_server
        self.socket = connection

    def process(self):
        LOG.debug("Entering the char selection process")
