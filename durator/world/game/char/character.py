import random

from peewee import ( Model, IntegerField, FloatField, ForeignKeyField, CharField
                   , PeeweeException )

from durator.auth.account import Account
from durator.db.database import DB, db_connection
from pyshgck.logger import LOG


class CharacterFeatures(Model):

    skin        = IntegerField(default = 0)
    face        = IntegerField(default = 0)
    hair_style  = IntegerField(default = 0)
    hair_color  = IntegerField(default = 0)
    facial_hair = IntegerField(default = 0)

    class Meta(object):
        database = DB


class CharacterStats(Model):

    level      = IntegerField(default = 1)
    experience = IntegerField(default = 0)

    class Meta(object):
        database = DB


class CharacterPosition(Model):

    map_id      = IntegerField(default = 0)
    zone_id     = IntegerField(default = 1)
    pos_x       = FloatField(default = 0.0)
    pos_y       = FloatField(default = 0.0)
    pos_z       = FloatField(default = 0.0)
    orientation = FloatField(default = 0.0)

    class Meta(object):
        database = DB


class Character(Model):

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


class CharacterManager(Model):

    @staticmethod
    @db_connection
    def create_character(account, char_values):
        """ Try to create a new character and add it to the database. Return 0
        on success, 1 on unspecified failure, 2 on name already used.

        The arg char_values is a tuple containing the Character data in the
        order they're defined, from name to features. This last value has to be
        a tuple with CharacterFeatures fields values.

        This should check of other things like account char limit etc.
        """
        name = char_values[0]
        name_exists = Character.select().where(Character.name == name).exists()
        if name_exists:
            LOG.debug("Name " + name + " already used.")
            return 2

        try:
            character = Character(
                guid = CharacterManager._get_unused_guid(), account = account,
                name = name, race = char_values[1].value,
                class_id = char_values[2].value, gender = char_values[3].value
            )

            features_tuple = char_values[4]
            features = CharacterFeatures.create(
                skin = features_tuple[0], face = features_tuple[1],
                hair_style = features_tuple[2], hair_color = features_tuple[3],
                facial_hair = features_tuple[4]
            )
            character.features = features

            character.stats = CharacterStats.create()
            character.position = CharacterPosition.create()

            character.save()
        except PeeweeException as exc:
            LOG.error("An error occured while creating character: " + str(exc))
            return 1

        LOG.debug("Character " + name + " created.")
        return 0

    @staticmethod
    @db_connection
    def _get_unused_guid():
        guid = -1
        while ( guid == -1
                or Character.select().where(Character.guid == guid).exists() ):
            guid = random.randrange(2**20)
        return guid

    @staticmethod
    @db_connection
    def delete_character(guid):
        """ Try to delete character and all associated data from the database.
        Return 0 on success, 1 on error. """
        try:
            character = Character.get(Character.guid == guid)
            features = character.features
            stats = character.stats
            position = character.position
            character.delete_instance()
            features.delete_instance()
            stats.delete_instance()
            position.delete_instance()
        except PeeweeException as exc:
            LOG.error("An error occured while deleting character {}: {}".format(
                guid, str(exc)
            ))
            return 1

        LOG.debug("Character " + str(guid) + " deleted.")
        return 0
