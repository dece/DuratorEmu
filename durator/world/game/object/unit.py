""" A Unit is a BaseObject that can move, attack, etc. """

from enum import Enum

from durator.world.game.object.base_object import BaseObject
from durator.world.game.object.object_fields import UnitField


class Bytes0Mask(Enum):

    RACE   = 0x000000FF
    CLASS  = 0x0000FF00
    GENDER = 0x00FF0000
    UNK    = 0xFF000000


class Unit(BaseObject):
    
    def get_race(self):
        unit_bytes_0 = self.get_bytes_0()
        return unit_bytes_0 & Bytes0Mask.RACE.value

    def get_class(self):
        unit_bytes_0 = self.get_bytes_0()
        return (unit_bytes_0 & Bytes0Mask.CLASS.value) >> 8

    def get_gender(self):
        unit_bytes_0 = self.get_bytes_0()
        return (unit_bytes_0 & Bytes0Mask.GENDER.value) >> 16

    def get_bytes_0(self):
        unit_bytes_0 = self.get(UnitField.BYTES_0)
        return unit_bytes_0 or 0
