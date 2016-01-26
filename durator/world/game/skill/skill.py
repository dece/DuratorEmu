from peewee import Model, IntegerField, ForeignKeyField

from durator.world.game.character.character_data import CharacterData
from durator.db.database import DB


class Skill(Model):
    """ Player skill. Max values shouldn't be stored in the database but we're
    reaching the end of development and I'm getting lazy. """

    character      = ForeignKeyField(CharacterData)
    ident          = IntegerField()
    level          = IntegerField(default = 0)
    max_level      = IntegerField(default = 0)
    stat_level     = IntegerField(default = 0)
    max_stat_level = IntegerField(default = 0)

    class Meta(object):
        database = DB
