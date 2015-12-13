from peewee import Model, IntegerField, ForeignKeyField, CharField

from durator.auth.account import Account
from durator.db.database import DB


class Character(Model):

    guid     = IntegerField()
    account  = ForeignKeyField(Account, related_name = "chars")
    name     = CharField(max_length = 12)
    race     = IntegerField()
    class_id = IntegerField()  # Have to add id because class is a reserved word
    gender   = IntegerField()

    class Meta(object):
        database = DB
