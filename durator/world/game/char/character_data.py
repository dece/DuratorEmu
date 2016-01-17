""" A bunch of models to define character data.

Values aren't stored in a single big model but are spreaded across smaller
models. This way, when accessing data with Peewee (the ORM engine), we can
preload bunches of values that are usually used together.
"""

import random

from peewee import (
    Model, IntegerField, FloatField, ForeignKeyField, CharField,
    PeeweeException )

from durator.auth.account import Account
from durator.world.game.char.constants import (
    CharacterGender, NEW_CHAR_CONSTS, RACE_AND_CLASS_CONSTS )
from durator.db.database import DB, db_connection
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

    level            = IntegerField(default = NEW_CHAR_CONSTS["level"])
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

    bytes_1 = IntegerField(default = 0)

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

    bytes_2 = IntegerField(default = 0)

    ranged_attack_power      = IntegerField(default = 0)
    ranged_attack_power_mods = IntegerField(default = 0)
    min_ranged_damage        = IntegerField(default = 0)
    max_ranged_damage        = IntegerField(default = 0)

    player_flags = IntegerField(default = 0)

    rest_info = IntegerField(default = NEW_CHAR_CONSTS["rest_info"])

    exp            = IntegerField(default = NEW_CHAR_CONSTS["exp"])
    next_level_exp = IntegerField(default = NEW_CHAR_CONSTS["next_level_exp"])

    character_points_1 = IntegerField(default = 0)
    character_points_2 = IntegerField(default = NEW_CHAR_CONSTS["prof_left"])

    block_percentage = FloatField(default = 4.0)
    dodge_percentage = FloatField(default = 4.0)
    parry_percentage = FloatField(default = 4.0)
    crit_percentage  = FloatField(default = 4.0)

    rest_state_exp = IntegerField(default = NEW_CHAR_CONSTS["rest_state_exp"])
    coinage        = IntegerField(default = NEW_CHAR_CONSTS["coinage"])

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





class CharacterManager(object):
    """ Transfer player character data between the database and the server. """

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
        name = char_values["name"]
        name_exists = CharacterManager.does_char_with_name_exist(name)
        if name_exists:
            LOG.debug("Name " + name + " already used.")
            return 2

        try:
            character = CharacterData(
                guid     = CharacterManager._get_unused_guid(),
                account  = account,
                name     = name,
                race     = char_values["race"].value,
                class_id = char_values["class"].value,
                gender   = char_values["gender"].value
            )

            features = CharacterFeatures.create(
                skin        = char_values["features"]["skin"],
                face        = char_values["features"]["face"],
                hair_style  = char_values["features"]["hair_style"],
                hair_color  = char_values["features"]["hair_color"],
                facial_hair = char_values["features"]["facial_hair"]
            )
            character.features = features

            race_and_class = (char_values["race"], char_values["class"])
            consts = RACE_AND_CLASS_CONSTS[race_and_class]
            gender = char_values["gender"]

            stats = CharacterManager._get_char_stats(consts, gender)
            position = CharacterManager._get_char_position(consts)
            character.stats = stats
            character.position = position

            character.save()
        except PeeweeException as exc:
            LOG.error("An error occured while creating character: " + str(exc))
            return 1

        LOG.debug("Character " + name + " created.")
        return 0

    @staticmethod
    def _get_unused_guid():
        guid = -1
        while guid == -1 or CharacterManager.does_char_with_guid_exist(guid):
            guid = random.randrange(0xFFFFFFFF)
        return guid

    @staticmethod
    def _get_char_stats(consts, gender):
        if gender == CharacterGender.MALE:
            model = consts["race"]["model_male"]
        else:
            model = consts["race"]["model_female"]

        return CharacterStats.create(
            scale_x = consts["race"]["scale_x"],

            health    = consts["class"]["max_health"],
            mana      = consts["class"]["max_power_mana"],
            rage      = consts["class"]["max_power_rage"],
            focus     = consts["class"]["max_power_focus"],
            energy    = consts["class"]["max_power_energy"],
            happiness = consts["class"]["max_power_happiness"],

            max_health    = consts["class"]["max_health"],
            max_mana      = consts["class"]["max_power_mana"],
            max_rage      = consts["class"]["max_power_rage"],
            max_focus     = consts["class"]["max_power_focus"],
            max_energy    = consts["class"]["max_power_energy"],
            max_happiness = consts["class"]["max_power_happiness"],

            level            = NEW_CHAR_CONSTS["level"],
            faction_template = consts["race"]["faction_template"],
            unit_flags       = NEW_CHAR_CONSTS["unit_flags"],

            attack_time_mainhand = consts["class"]["attack_time_mainhand"],
            attack_time_offhand  = consts["class"]["attack_time_offhand"],
            attack_time_ranged   = consts["class"]["attack_time_ranged"],

            bounding_radius = consts["race"]["bounding_radius"],
            combat_reach    = consts["race"]["combat_reach"],

            display_id        = model,
            native_display_id = model,

            min_damage         = consts["class"]["min_damage"],
            max_damage         = consts["class"]["max_damage"],
            min_offhand_damage = consts["class"]["min_offhand_damage"],
            max_offhand_damage = consts["class"]["max_offhand_damage"],

            unit_bytes_1 = NEW_CHAR_CONSTS["unit_bytes_1"],

            mod_cast_speed = consts["class"]["mod_cast_speed"],

            strength  = consts["class"]["stat_strength"],
            agility   = consts["class"]["stat_agility"],
            stamina   = consts["class"]["stat_stamina"],
            intellect = consts["class"]["stat_intellect"],
            spirit    = consts["class"]["stat_spirit"],

            resistance_0 = NEW_CHAR_CONSTS["resistances"],
            resistance_1 = NEW_CHAR_CONSTS["resistances"],
            resistance_2 = NEW_CHAR_CONSTS["resistances"],
            resistance_3 = NEW_CHAR_CONSTS["resistances"],
            resistance_4 = NEW_CHAR_CONSTS["resistances"],
            resistance_5 = NEW_CHAR_CONSTS["resistances"],
            resistance_6 = NEW_CHAR_CONSTS["resistances"],

            attack_power      = consts["class"]["attack_power"],
            base_mana         = consts["class"]["base_mana"],
            attack_power_mods = consts["class"]["attack_power_mod"],

            bytes_2 = NEW_CHAR_CONSTS["unit_bytes_2"],

            ranged_attack_power      = consts["class"]["ap_ranged"],
            ranged_attack_power_mods = consts["class"]["ap_ranged_mod"],
            min_ranged_damage        = consts["class"]["min_ranged_damage"],
            max_ranged_damage        = consts["class"]["max_ranged_damage"],

            player_flags = NEW_CHAR_CONSTS["player_flags"],

            rest_info = NEW_CHAR_CONSTS["rest_info"],

            exp            = NEW_CHAR_CONSTS["exp"],
            next_level_exp = NEW_CHAR_CONSTS["next_level_exp"],

            character_points_1 = NEW_CHAR_CONSTS["character_points_1"],
            character_points_2 = NEW_CHAR_CONSTS["prof_left"],

            block_percentage = NEW_CHAR_CONSTS["block_percentage"],
            dodge_percentage = NEW_CHAR_CONSTS["dodge_percentage"],
            parry_percentage = NEW_CHAR_CONSTS["parry_percentage"],
            crit_percentage  = NEW_CHAR_CONSTS["crit_percentage"],

            rest_state_exp = NEW_CHAR_CONSTS["rest_state_exp"],
            coinage        = NEW_CHAR_CONSTS["coinage"]
        )

    @staticmethod
    def _get_char_position(consts):
        return CharacterPosition.create(
            map_id      = consts["race"]["start_map"],
            zone_id     = consts["race"]["start_zone"],
            pos_x       = consts["race"]["start_pos_x"],
            pos_y       = consts["race"]["start_pos_y"],
            pos_z       = consts["race"]["start_pos_z"],
            orientation = consts["race"]["start_orientation"]
        )

    @staticmethod
    @db_connection
    def does_char_with_name_exist(name):
        return ( CharacterData
                 .select()
                 .where(CharacterData.name == name)
                 .exists() )

    @staticmethod
    @db_connection
    def does_char_with_guid_exist(guid):
        return ( CharacterData
                 .select()
                 .where(CharacterData.guid == guid)
                 .exists() )

    @staticmethod
    @db_connection
    def delete_character(guid):
        """ Try to delete character and all associated data from the database.
        Return 0 on success, 1 on error. """
        try:
            character = CharacterData.get(CharacterData.guid == guid)
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
