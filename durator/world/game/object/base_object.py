from enum import Enum

from durator.world.game.object.object_fields import ObjectField
from durator.world.game.position import Position


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


class ObjectTypeFlags(Enum):
    """ BaseObject descriptors "flags" (field 0x8). """

    OBJECT         = 1 << 0
    ITEM           = 1 << 1
    CONTAINER      = 1 << 2
    UNIT           = 1 << 3
    PLAYER         = 1 << 4
    GAME_OBJECT    = 1 << 5
    DYNAMIC_OBJECT = 1 << 6
    CORPSE         = 1 << 7


OBJECT_TYPE_TO_FLAGS = {
    ObjectType.OBJECT:         ( ObjectTypeFlags.OBJECT ),
    ObjectType.ITEM:           ( ObjectTypeFlags.OBJECT |
                                   ObjectTypeFlags.ITEM ),
    ObjectType.CONTAINER:      ( ObjectTypeFlags.OBJECT      |
                                   ObjectTypeFlags.ITEM      |
                                   ObjectTypeFlags.CONTAINER ),
    ObjectType.UNIT:           ( ObjectTypeFlags.OBJECT |
                                   ObjectTypeFlags.UNIT ),
    ObjectType.PLAYER:         ( ObjectTypeFlags.OBJECT   |
                                   ObjectTypeFlags.UNIT   |
                                   ObjectTypeFlags.PLAYER ),
    ObjectType.GAME_OBJECT:    ( ObjectTypeFlags.OBJECT        |
                                   ObjectTypeFlags.GAME_OBJECT ),
    ObjectType.DYNAMIC_OBJECT: ( ObjectTypeFlags.OBJECT           |
                                   ObjectTypeFlags.DYNAMIC_OBJECT ),
    ObjectType.CORPSE:         ( ObjectTypeFlags.OBJECT   |
                                   ObjectTypeFlags.CORPSE )
}

OBJECT_FLAGS_TO_TYPE = {
    ( ObjectTypeFlags.OBJECT ):           ObjectType.OBJECT,
    ( ObjectTypeFlags.OBJECT |
        ObjectTypeFlags.ITEM ):           ObjectType.ITEM,
    ( ObjectTypeFlags.OBJECT      |
        ObjectTypeFlags.ITEM      |
        ObjectTypeFlags.CONTAINER ):      ObjectType.CONTAINER,
    ( ObjectTypeFlags.OBJECT |
        ObjectTypeFlags.UNIT ):           ObjectType.UNIT,
    ( ObjectTypeFlags.OBJECT   |
        ObjectTypeFlags.UNIT   |
        ObjectTypeFlags.PLAYER ):         ObjectType.PLAYER,
    ( ObjectTypeFlags.OBJECT        |
        ObjectTypeFlags.GAME_OBJECT ):    ObjectType.GAME_OBJECT,
    ( ObjectTypeFlags.OBJECT           |
        ObjectTypeFlags.DYNAMIC_OBJECT ): ObjectType.DYNAMIC_OBJECT,
    ( ObjectTypeFlags.OBJECT   |
        ObjectTypeFlags.CORPSE ):         ObjectType.CORPSE
}



class BaseObject(object):
    """ A BaseObject is the base type for all things spawned in world.

    It has a name that can be queried by clients, map and zone IDs, a Position,
    and a dict of fields with their associated values.
    """

    def __init__(self):
        self.name = "Unnamed object"
        self.map_id = 0
        self.zone_id = 0
        self.position = Position()
        self.fields = {}

    @property
    def guid(self):
        return self.get(ObjectField.GUID)

    @property
    def type(self):
        flags = self.get(ObjectField.TYPE)  # misleading field name
        return ObjectType(OBJECT_FLAGS_TO_TYPE[flags])

    def get(self, field):
        """ Return the object field value, or None if it hasn't been set. """
        return self.fields.get(field)

    def set(self, field, value):
        """ Set a new object field value. """
        self.fields[field] = value
