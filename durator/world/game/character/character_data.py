""" A bunch of models to define character data.

Values aren't stored in a single big model but are spreaded across smaller
models. This way, when accessing data with Peewee (the ORM engine), we can
preload bunches of values that are usually used together.
"""

import random

from peewee import (
    Model, IntegerField, FloatField, ForeignKeyField, CharField,
    PeeweeException )

from durator.common.account.account import Account
from durator.db.database import DB, db_connection
from durator.world.game.character.constants import CharacterGender
from durator.world.game.character.defaults import (
    NEW_CHAR_DEFAULTS, RACE_AND_CLASS_DEFAULTS )
from pyshgck.logger import LOG


class CharacterFeatures(Model):
    """ Features specific to a player character. """

    skin        = IntegerField(default = 0)
    face        = IntegerField(default = 0)
    hair_style  = IntegerField(default = 0)
    hair_color  = IntegerField(default = 0)
    facial_hair = IntegerField(default = 0)

    class Meta(object):
        database = DB


class CharacterStats(Model):
    """ A big bunch of Unit and Player fields that have to be stored. """

    scale_x = FloatField(default = 1.0)

    health    = IntegerField()
    mana      = IntegerField()
    rage      = IntegerField()
    focus     = IntegerField()
    energy    = IntegerField()
    happiness = IntegerField()

    max_health    = IntegerField()
    max_mana      = IntegerField()
    max_rage      = IntegerField()
    max_focus     = IntegerField()
    max_energy    = IntegerField()
    max_happiness = IntegerField()

    level            = IntegerField(default = NEW_CHAR_DEFAULTS["level"])
    faction_template = IntegerField(default = 0)
    unit_flags       = IntegerField(default = 0)

    attack_time_mainhand = IntegerField(default = 2000)
    attack_time_offhand  = IntegerField(default = 2000)
    attack_time_ranged   = IntegerField(default = 2000)

    bounding_radius = FloatField(default = 1.0)
    combat_reach    = FloatField(default = 1.0)

    display_id        = IntegerField()
    native_display_id = IntegerField()
    mount_display_id  = IntegerField(default = 0)

    min_damage         = IntegerField(default = 0)
    max_damage         = IntegerField(default = 0)
    min_offhand_damage = IntegerField(default = 0)
    max_offhand_damage = IntegerField(default = 0)

    unit_bytes_1 = IntegerField(default = 0)

    mod_cast_speed = IntegerField(default = 1)

    strength  = IntegerField(default = 0)
    agility   = IntegerField(default = 0)
    stamina   = IntegerField(default = 0)
    intellect = IntegerField(default = 0)
    spirit    = IntegerField(default = 0)

    resistance_0 = IntegerField(default = 0)
    resistance_1 = IntegerField(default = 0)
    resistance_2 = IntegerField(default = 0)
    resistance_3 = IntegerField(default = 0)
    resistance_4 = IntegerField(default = 0)
    resistance_5 = IntegerField(default = 0)
    resistance_6 = IntegerField(default = 0)

    attack_power      = IntegerField(default = 0)
    base_mana         = IntegerField(default = 1)
    attack_power_mods = IntegerField(default = 0)

    unit_bytes_2 = IntegerField(default = 0)

    ranged_attack_power      = IntegerField(default = 0)
    ranged_attack_power_mods = IntegerField(default = 0)
    min_ranged_damage        = IntegerField(default = 0)
    max_ranged_damage        = IntegerField(default = 0)

    player_flags = IntegerField(default = 0)

    rest_info = IntegerField(default = NEW_CHAR_DEFAULTS["rest_info"])

    exp            = IntegerField(default = NEW_CHAR_DEFAULTS["exp"])
    next_level_exp = IntegerField(default = NEW_CHAR_DEFAULTS["next_level_exp"])

    character_points_1 = IntegerField(default = 0)
    character_points_2 = IntegerField(default = NEW_CHAR_DEFAULTS["prof_left"])

    block_percentage = FloatField(default = 4.0)
    dodge_percentage = FloatField(default = 4.0)
    parry_percentage = FloatField(default = 4.0)
    crit_percentage  = FloatField(default = 4.0)

    rest_state_exp = IntegerField(default = NEW_CHAR_DEFAULTS["rest_state_exp"])
    coinage        = IntegerField(default = NEW_CHAR_DEFAULTS["coinage"])

    class Meta(object):
        database = DB


class CharacterPosition(Model):
    """ Coordinates in the world. Probably should be more abstract. """

    map_id      = IntegerField(default = 0)
    zone_id     = IntegerField(default = 1)
    pos_x       = FloatField(default = 0.0)
    pos_y       = FloatField(default = 0.0)
    pos_z       = FloatField(default = 0.0)
    orientation = FloatField(default = 0.0)

    class Meta(object):
        database = DB


class CharacterData(Model):
    """ Main model containing data (and foreign keys to more data) to all the
    stuff the makes a character. """

    guid     = IntegerField(unique = True)
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
