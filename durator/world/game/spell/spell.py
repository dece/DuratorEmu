from peewee import Model, IntegerField, ForeignKeyField

from durator.world.game.character.character_data import CharacterData
from durator.db.database import DB


class Spell(Model):

    character      = ForeignKeyField(CharacterData)
    ident          = IntegerField()

    class Meta(object):
        database = DB
