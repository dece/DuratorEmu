""" Constants for characters, races and classes. """

from enum import Enum


class CharacterRace(Enum):

    HUMAN     = 1
    ORC       = 2
    DWARF     = 3
    NIGHT_ELF = 4
    UNDEAD    = 5
    TAUREN    = 6
    GNOME     = 7
    TROLL     = 8


class CharacterClass(Enum):

    NONE    = 0
    WARRIOR = 1
    PALADIN = 2
    HUNTER  = 3
    ROGUE   = 4
    PRIEST  = 5
    SHAMAN  = 7
    MAGE    = 8
    WARLOCK = 9
    DRUID   = 11


class CharacterGender(Enum):

    MALE   = 0
    FEMALE = 1


class CharacterEquipSlot(Enum):

    HEAD      = 0
    NECK      = 1
    SHOULDERS = 2
    BODY      = 3
    CHEST     = 4
    WAIST     = 5
    LEGS      = 6
    FEET      = 7
    WRISTS    = 8
    HANDS     = 9
    FINGER1   = 10
    FINGER2   = 11
    TRINKET1  = 12
    TRINKET2  = 13
    BACK      = 14
    MAINHAND  = 15
    OFFHAND   = 16
    RANGED    = 17
    TABARD    = 18
    BAG1      = 19
    BAG2      = 20
    BAG3      = 21
    BAG4      = 22
