""" A BaseObject is the base type for all things spawned in world.

This module defines a class that can hold a value for each object field, and a
set of subclasses specific to each type of object discerned by the game.
"""

from enum import Enum


class ObjectType(Enum):
    """ Object type sent in UpdateObject packets, with associated flags. """

    OBJECT         = 0  # 0x01 (object)
    ITEM           = 1  # 0x03 (object, item)
    CONTAINER      = 2  # 0x07 (object, item, container)
    UNIT           = 3  # 0x09 (object, unit)
    PLAYER         = 4  # 0x19 (object, unit, player)
    GAME_OBJECT    = 5  # 0x21 (object, game_object)
    DYNAMIC_OBJECT = 6  # 0x41 (object, dynamic_object)
    CORPSE         = 7  # 0x81 (object, corpse)


class ObjectDescFlags(Enum):
    """ BaseObject descriptors "flags" (field 0x8). """

    OBJECT         = 1 << 0
    ITEM           = 1 << 1
    CONTAINER      = 1 << 2
    UNIT           = 1 << 3
    PLAYER         = 1 << 4
    GAME_OBJECT    = 1 << 5
    DYNAMIC_OBJECT = 1 << 6
    CORPSE         = 1 << 7


class BaseObject(object):

    def __init__(self):
        self.fields = {}

    def get(self, field):
        """ Return the object field value, or None if it hasn't been set. """
        return self.fields.get(field)

    def set(self, field, value):
        """ Set a new object field value. """
        self.fields[field] = value


class ItemObject(BaseObject):
    pass


class ContainerObject(ItemObject):
    pass


class UnitObject(BaseObject):
    pass


class PlayerObject(UnitObject):
    pass


class GameObject(BaseObject):
    pass


class DynamicObject(BaseObject):
    pass


class CorpseObject(BaseObject):
    pass
