from peewee import Model, IntegerField, ForeignKeyField

from durator.world.game.character.character_data import CharacterData
from durator.db.database import DB


class Skill(Model):
    """ Features specific to a player character. """

    character      = ForeignKeyField(CharacterData)
    ident          = IntegerField()
    level          = IntegerField(default = 0)
    max_level      = IntegerField(default = 0)
    stat_level     = IntegerField(default = 0)
    max_stat_level = IntegerField(default = 0)

    class Meta(object):
        database = DB
