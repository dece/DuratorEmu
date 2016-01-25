import threading

from pyshgck.logger import LOG


def members_lock(func):
    def members_lock_decorator(self, *args, **kwargs):
        with self.members_lock:
            return func(self, *args, **kwargs)
    return members_lock_decorator


class Channel(object):
    """ Channels must be handled by the ChatManager only. Immutable objects
    can be accessed thread-safely. """

    def __init__(self, name, password = "", internal_id = 0):
        self.name = name
        self.password = password
        self.internal_id = internal_id
        self.members = []
        self.members_lock = threading.Lock()

    @members_lock
    def _add_member(self, guid):
        self.members.append(guid)

    def add_member(self, player):
        guid = player.guid
        if guid not in self.members:
            LOG.info("{} joins channel '{}'.".format(player.name, self.name))
            self._add_member(guid)

    @members_lock
    def get_members(self):
        return list(self.members)
