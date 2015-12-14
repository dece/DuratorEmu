from enum import Enum

from peewee import Model, IntegerField, FloatField, ForeignKeyField, CharField

from durator.auth.account import Account
from durator.db.database import DB


class CharacterRace(Enum):

    HUMAN = 1
    ORC = 2
    DWARF = 3
    NIGHT_ELF = 4
    UNDEAD = 5
    TAUREN = 6
    GNOME = 7
    TROLL = 8
    GOBLIN = 9
    BLOOD_ELF = 10
    DRAENEI = 11
    FEL_ORC = 12
    NAGA = 13
    BROKEN = 14
    SKELETON = 15


class CharacterClass(Enum):

    NONE = 0
    WARRIOR = 1
    PALADIN = 2
    HUNTER = 3
    ROGUE = 4
    PRIEST = 5
    DEATH_KNIGHT = 6
    SHAMAN = 7
    MAGE = 8
    WARLOCK = 9
    DRUID = 11


class CharacterEquipSlot(Enum):

    HEAD = 0
    NECK = 1
    SHOULDERS = 2
    BODY = 3
    CHEST = 4
    WAIST = 5
    LEGS = 6
    FEET = 7
    WRISTS = 8
    HANDS = 9
    FINGER1 = 10
    FINGER2 = 11
    TRINKET1 = 12
    TRINKET2 = 13
    BACK = 14
    MAINHAND = 15
    OFFHAND = 16
    RANGED = 17
    TABARD = 18
    BAG1 = 19
    BAG2 = 20
    BAG3 = 21
    BAG4 = 22


class CharacterFeatures(Model):

    skin        = IntegerField()
    face        = IntegerField()
    hair_style  = IntegerField()
    hair_color  = IntegerField()
    facial_hair = IntegerField()

    class Meta(object):
        database = DB


class CharacterStats(Model):

    level      = IntegerField()
    experience = IntegerField()

    class Meta(object):
        database = DB


class CharacterPosition(Model):

    map_id  = IntegerField()
    zone_id = IntegerField()
    pos_x   = FloatField()
    pos_y   = FloatField()
    pos_z   = FloatField()

    class Meta(object):
        database = DB


class Character(Model):

    guid     = IntegerField()
    account  = ForeignKeyField(Account, related_name = "chars")
    name     = CharField(max_length = 12)
    race     = IntegerField()
    class_id = IntegerField()
    gender   = IntegerField()
    features = ForeignKeyField(CharacterFeatures)
    stats    = ForeignKeyField(CharacterStats)
    position = ForeignKeyField(CharacterPosition)

    class Meta(object):
        database = DB
