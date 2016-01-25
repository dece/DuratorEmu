""" Simple chat manager. Does not handle localisation or anything. """

import threading

from pyshgck.logger import LOG


INTERNAL_NAME_PREFIX_MAP = {
    "General - ":      1,
    "Trade - ":        2,
    "LocalDefense - ": 3
}


def channels_lock(func):
    def channels_lock_decorator(self, *args, **kwargs):
        with self.channels_lock:
            return func(self, *args, **kwargs)
    return channels_lock_decorator


class ChatManager(object):

    def __init__(self):
        self.channels = {}
        self.channels_lock = threading.Lock()

    def create_channel(self, name, password = ""):
        """ Try to create a channel.

        Return 0 on success, 1 if a channel with that name already exists.
        """
        if name not in self.channels:
            internal_id = ChatManager.get_internal_channel_id(name)
            channel = Channel(name, password, internal_id)
            self._add_channel(channel)
            return 0
        else:
            return 1

    @channels_lock
    def _add_channel(self, channel):
        self.channels[channel.name] = channel

    @staticmethod
    def get_internal_channel_id(name):
        for prefix in INTERNAL_NAME_PREFIX_MAP:
            if name.startswith(prefix):
                return INTERNAL_NAME_PREFIX_MAP[prefix]
        return 0

    @channels_lock
    def get_channel(self, name):
        return self.channels.get(name)

    @channels_lock
    def get_channels_names(self):
        return list(self.channels)

    def join(self, player, chan_name, password):
        """ Try to add player to this channel with this password.

        Return 0 on success, 1 if the password is wrong.
        """
        if chan_name not in self.channels:
            self.create_channel(chan_name, password)

        # This call assumes that after create_channel, the chan always exists.
        channel = self.get_channel(chan_name)
        if password == channel.password:
            channel.add_member(player)
            return 0
        else:
            self.clean(chan_name)
            return 1

    def clean(self, chan_name = None):
        """ Remove all empty channels, or chan_name if provided. """
        if chan_name is not None:
            self._delete_channel_if_empty(chan_name)
        else:
            channels_names = self.get_channels_names()
            for chan_name in channels_names:
                self._delete_channel_if_empty(chan_name)

    def _delete_channel_if_empty(self, name):
        channel = self.get_channel(name)
        if channel is None:
            return
        if not channel.members:
            self._remove_channel(name)

    @channels_lock
    def _remove_channel(self, name):
        del self.channels[name]


class Channel(object):
    """ Channels must be handled by the ChatManager only. Immutable objects
    can be accessed thread-safely. """

    def __init__(self, name, password = "", internal_id = 0):
        self.name = name
        self.password = password
        self.internal_id = internal_id
        self.members = []

    def add_member(self, player):
        guid = player.guid
        if guid not in self.members:
            self.members.append(guid)
            LOG.info("{} joins channel {}.".format(player.name, self.name))

    def receive_message(self, message):
        pass
