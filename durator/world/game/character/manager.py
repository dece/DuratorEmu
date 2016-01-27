import random

from peewee import PeeweeException

from durator.db.database import db_connection
from durator.world.game.character.character_data import (
    CharacterData, CharacterFeatures, CharacterStats, CharacterPosition )
from durator.world.game.character.constants import CharacterGender
from durator.world.game.character.defaults import (
    NEW_CHAR_DEFAULTS, RACE_AND_CLASS_DEFAULTS )
from durator.world.game.skill.skill import Skill
from durator.world.game.skill.defaults import SKILL_MAX_LEVELS
from pyshgck.logger import LOG


class CharacterManager(object):
    """ Transfer player character data between the database and the server. """

    @staticmethod
    def create_character(account, char_values):
        """ See CharacterCreator.create_character. """
        return _CharacterCreator.create_character(account, char_values)

    @staticmethod
    @db_connection
    def get_char_data(guid):
        """ Get the CharacterData associated to that GUID, or None. """
        try:
            return CharacterData.get(CharacterData.guid == guid)
        except CharacterData.DoesNotExist:
            return None

    @staticmethod
    @db_connection
    def does_char_with_name_exist(name):
        """ Return whether or not a character with that name exists in DB. """
        return ( CharacterData
                 .select()
                 .where(CharacterData.name == name)
                 .exists() )

    @staticmethod
    @db_connection
    def does_char_with_guid_exist(guid):
        """ Return whether or not a character with that GUID exists in DB. """
        return ( CharacterData
                 .select()
                 .where(CharacterData.guid == guid)
                 .exists() )

    @staticmethod
    def delete_character(guid):
        """ See CharacterDestructor.delete_character. """
        return _CharacterDestructor.delete_character(guid)


class _CharacterCreator(object):

    @staticmethod
    @db_connection
    def create_character(account, char_values):
        """ Try to create a new character and add it to the database. Return 0
        on success, 1 on unspecified failure, 2 on name already used, 3 if the
        race and class combination isn't supported.

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
                guid     = _CharacterCreator._get_unused_guid(),
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
            consts = RACE_AND_CLASS_DEFAULTS.get(race_and_class)
            if consts is None:
                return 3
            gender = char_values["gender"]

            stats = _CharacterCreator._get_default_char_stats(consts, gender)
            position = _CharacterCreator._get_default_char_position(consts)
            character.stats = stats
            character.position = position

            character.save()

            _CharacterCreator._add_default_skills(character, consts)
        except PeeweeException as exc:
            LOG.error("An error occured while creating character: " + str(exc))
            return 1

        LOG.debug("Character " + name + " created.")
        return 0

    @staticmethod
    def _get_unused_guid():
        guid = -1
        while guid == -1 or CharacterManager.does_char_with_guid_exist(guid):
            guid = random.randrange(0x00FFFFFF)
        return guid

    @staticmethod
    def _get_default_char_stats(consts, gender):
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

            level            = NEW_CHAR_DEFAULTS["level"],
            faction_template = consts["race"]["faction_template"],
            unit_flags       = NEW_CHAR_DEFAULTS["unit_flags"],

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

            unit_bytes_1 = NEW_CHAR_DEFAULTS["unit_bytes_1"],

            mod_cast_speed = consts["class"]["mod_cast_speed"],

            strength  = consts["class"]["stat_strength"],
            agility   = consts["class"]["stat_agility"],
            stamina   = consts["class"]["stat_stamina"],
            intellect = consts["class"]["stat_intellect"],
            spirit    = consts["class"]["stat_spirit"],

            resistance_0 = NEW_CHAR_DEFAULTS["resistances"],
            resistance_1 = NEW_CHAR_DEFAULTS["resistances"],
            resistance_2 = NEW_CHAR_DEFAULTS["resistances"],
            resistance_3 = NEW_CHAR_DEFAULTS["resistances"],
            resistance_4 = NEW_CHAR_DEFAULTS["resistances"],
            resistance_5 = NEW_CHAR_DEFAULTS["resistances"],
            resistance_6 = NEW_CHAR_DEFAULTS["resistances"],

            attack_power      = consts["class"]["attack_power"],
            base_mana         = consts["class"]["base_mana"],
            attack_power_mods = consts["class"]["attack_power_mod"],

            unit_bytes_2 = NEW_CHAR_DEFAULTS["unit_bytes_2"],

            ranged_attack_power      = consts["class"]["ap_ranged"],
            ranged_attack_power_mods = consts["class"]["ap_ranged_mod"],
            min_ranged_damage        = consts["class"]["min_ranged_damage"],
            max_ranged_damage        = consts["class"]["max_ranged_damage"],

            player_flags = NEW_CHAR_DEFAULTS["player_flags"],

            rest_info = NEW_CHAR_DEFAULTS["rest_info"],

            exp            = NEW_CHAR_DEFAULTS["exp"],
            next_level_exp = NEW_CHAR_DEFAULTS["next_level_exp"],

            character_points_1 = NEW_CHAR_DEFAULTS["character_points_1"],
            character_points_2 = NEW_CHAR_DEFAULTS["prof_left"],

            block_percentage = NEW_CHAR_DEFAULTS["block_percentage"],
            dodge_percentage = NEW_CHAR_DEFAULTS["dodge_percentage"],
            parry_percentage = NEW_CHAR_DEFAULTS["parry_percentage"],
            crit_percentage  = NEW_CHAR_DEFAULTS["crit_percentage"],

            rest_state_exp = NEW_CHAR_DEFAULTS["rest_state_exp"],
            coinage        = NEW_CHAR_DEFAULTS["coinage"]
        )

    @staticmethod
    def _get_default_char_position(consts):
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
    def _add_default_skills(char_data, consts):
        skills = consts["class"]["skills"]
        for skill in skills:
            values = skills[skill]
            max_values = SKILL_MAX_LEVELS[skill]
            Skill.create(
                character      = char_data,
                ident          = skill.value,

                level          = values[0],
                stat_level     = values[1],

                max_level      = max_values[0],
                max_stat_level = max_values[1]
            )


class _CharacterDestructor(object):

    @staticmethod
    @db_connection
    def delete_character(guid):
        """ Try to delete character and all associated data from the database.
        Return 0 on success, 1 on error. """
        try:
            character = CharacterData.get(CharacterData.guid == guid)

            _CharacterDestructor._delete_char_skills(character)

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

    @staticmethod
    @db_connection
    def _delete_char_skills(character):
        Skill.delete().where(Skill.character == character).execute()
