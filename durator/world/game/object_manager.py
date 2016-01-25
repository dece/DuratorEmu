import threading

from durator.world.game.character.character_data import CharacterManager
from durator.world.game.object.base_object import ObjectDescFlags
from durator.world.game.object.object_fields import (
    ObjectField, UnitField, PlayerField )
from durator.world.game.object.player import Player
from pyshgck.logger import LOG


class ObjectManager(object):
    """ Manage all objects in world. To avoid an overcrowded class, boring
    stuff is moved to friend classes. """

    def __init__(self):
        self.players = {}
        self.locks = { lock_name: threading.Lock() for lock_name in
                       ["players"] }

    def add_player(self, char_data):
        """ Create (and return) a Player object from the data stored in the
        database, and add it to the managed object list. """
        player = Player()
        player.name = char_data.name

        ObjectManager._add_coords_to_object(player, char_data.position)
        _PlayerManager.add_object_fields(player, char_data)
        _PlayerManager.add_unit_fields(player, char_data)
        _PlayerManager.add_player_fields(player, char_data)

        with self.locks["players"]:
            self.players[player.guid] = player

        return player

    @staticmethod
    def _add_coords_to_object(base_object, position_data):
        base_object.map_id     = position_data.map_id
        base_object.zone_id    = position_data.zone_id
        base_object.position.x = position_data.pos_x
        base_object.position.y = position_data.pos_y
        base_object.position.z = position_data.pos_z
        base_object.position.o = position_data.orientation

    def get_player(self, guid):
        """ Return the object with that GUID, or None if it doesn't exist. """
        with self.locks["players"]:
            return self.players.get(guid)

    @staticmethod
    def _get_coords_from_object(base_object, position_data):
        position_data.map_id      = base_object.map_id
        position_data.zone_id     = base_object.zone_id
        position_data.pos_x       = base_object.position.x
        position_data.pos_y       = base_object.position.y
        position_data.pos_z       = base_object.position.z
        position_data.orientation = base_object.position.o

    def remove_player(self, guid):
        """ Remove the player from the object list and save its data. """
        player = self.get_player(guid)
        if player is None:
            LOG.warning("Tried to remove a non-existing player.")
            return

        with self.locks["players"]:
            del self.players[guid]

        char_data = CharacterManager.get_char_data(guid)
        ObjectManager._get_coords_from_object(player, char_data.position)
        _PlayerManager.get_object_fields(player, char_data)
        _PlayerManager.get_unit_fields(player, char_data)
        _PlayerManager.get_player_fields(player, char_data)

        char_data.features.save()
        char_data.stats.save()
        char_data.position.save()
        char_data.save()


class _PlayerManager(object):
    """ Static methods to transfer data from database models to objects. """

    @staticmethod
    def add_object_fields(player, char_data):
        object_type = (
            ObjectDescFlags.OBJECT.value |
            ObjectDescFlags.UNIT.value   |
            ObjectDescFlags.PLAYER.value
        )
        player.set(ObjectField.GUID,    char_data.guid)
        player.set(ObjectField.TYPE,    object_type)
        player.set(ObjectField.SCALE_X, char_data.stats.scale_x)

    @staticmethod
    def add_unit_fields(player, char_data):
        stats = char_data.stats

        player.set(UnitField.HEALTH,  stats.health)
        player.set(UnitField.POWER_1, stats.mana)
        player.set(UnitField.POWER_2, stats.rage)
        player.set(UnitField.POWER_3, stats.focus)
        player.set(UnitField.POWER_4, stats.energy)
        player.set(UnitField.POWER_5, stats.happiness)

        player.set(UnitField.MAX_HEALTH,  stats.max_health)
        player.set(UnitField.MAX_POWER_1, stats.max_mana)
        player.set(UnitField.MAX_POWER_2, stats.max_rage)
        player.set(UnitField.MAX_POWER_3, stats.max_focus)
        player.set(UnitField.MAX_POWER_4, stats.max_energy)
        player.set(UnitField.MAX_POWER_5, stats.max_happiness)

        unit_bytes_0 = (
            char_data.race          |
            char_data.class_id << 8 |
            char_data.gender << 16  |
            1 << 24
        )

        player.set(UnitField.LEVEL,            stats.level)
        player.set(UnitField.FACTION_TEMPLATE, stats.faction_template)
        player.set(UnitField.BYTES_0,          unit_bytes_0)
        player.set(UnitField.FLAGS,            stats.unit_flags)

        player.set(UnitField.BASE_ATTACK_TIME,    stats.attack_time_mainhand)
        player.set(UnitField.OFFHAND_ATTACK_TIME, stats.attack_time_offhand)

        player.set(UnitField.BOUNDING_RADIUS, stats.bounding_radius)
        player.set(UnitField.COMBAT_REACH,    stats.combat_reach)

        player.set(UnitField.DISPLAY_ID,        stats.display_id)
        player.set(UnitField.NATIVE_DISPLAY_ID, stats.native_display_id)
        player.set(UnitField.MOUNT_DISPLAY_ID,  stats.mount_display_id)

        player.set(UnitField.MIN_DAMAGE,         stats.min_damage)
        player.set(UnitField.MAX_DAMAGE,         stats.max_damage)
        player.set(UnitField.MIN_OFFHAND_DAMAGE, stats.min_offhand_damage)
        player.set(UnitField.MAX_OFFHAND_DAMAGE, stats.max_offhand_damage)

        player.set(UnitField.BYTES_1, stats.unit_bytes_1)

        player.set(UnitField.MOD_CAST_SPEED, stats.mod_cast_speed)

        player.set(UnitField.STAT_0,       stats.strength)
        player.set(UnitField.STAT_1,       stats.agility)
        player.set(UnitField.STAT_2,       stats.stamina)
        player.set(UnitField.STAT_3,       stats.intellect)
        player.set(UnitField.STAT_4,       stats.spirit)
        player.set(UnitField.RESISTANCE_0, stats.resistance_0)
        player.set(UnitField.RESISTANCE_1, stats.resistance_1)
        player.set(UnitField.RESISTANCE_2, stats.resistance_2)
        player.set(UnitField.RESISTANCE_3, stats.resistance_3)
        player.set(UnitField.RESISTANCE_4, stats.resistance_4)
        player.set(UnitField.RESISTANCE_5, stats.resistance_5)
        player.set(UnitField.RESISTANCE_6, stats.resistance_6)

        player.set(UnitField.ATTACK_POWER,      stats.attack_power)
        player.set(UnitField.BASE_MANA,         stats.base_mana)
        player.set(UnitField.ATTACK_POWER_MODS, stats.attack_power_mods)

        player.set(UnitField.BYTES_2, stats.unit_bytes_2)

        player.set(UnitField.RANGED_ATTACK_POWER,
            stats.ranged_attack_power)
        player.set(UnitField.RANGED_ATTACK_POWER_MODS,
            stats.ranged_attack_power_mods)
        player.set(UnitField.MIN_RANGED_DAMAGE, stats.min_ranged_damage)
        player.set(UnitField.MAX_RANGED_DAMAGE, stats.max_ranged_damage)

    @staticmethod
    def add_player_fields(player, char_data):
        stats = char_data.stats

        player.set(PlayerField.FLAGS, stats.player_flags)

        player_bytes_1 = (
            char_data.features.skin             |
            char_data.features.face << 8        |
            char_data.features.hair_style << 16 |
            char_data.features.hair_color << 24
        )
        player_bytes_2 = (
            char_data.features.facial_hair |
            stats.rest_info << 24
        )
        player_bytes_3 = char_data.gender

        player.set(PlayerField.BYTES_1, player_bytes_1)
        player.set(PlayerField.BYTES_2, player_bytes_2)
        player.set(PlayerField.BYTES_3, player_bytes_3)

        player.set(PlayerField.EXP,            stats.exp)
        player.set(PlayerField.NEXT_LEVEL_EXP, stats.next_level_exp)

        player.set(PlayerField.CHARACTER_POINTS_1, stats.character_points_1)
        player.set(PlayerField.CHARACTER_POINTS_2, stats.character_points_2)

        player.set(PlayerField.BLOCK_PERCENTAGE, stats.block_percentage)
        player.set(PlayerField.DODGE_PERCENTAGE, stats.dodge_percentage)
        player.set(PlayerField.PARRY_PERCENTAGE, stats.parry_percentage)
        player.set(PlayerField.CRIT_PERCENTAGE,  stats.crit_percentage)

        player.set(PlayerField.REST_STATE_EXP, stats.rest_state_exp)
        player.set(PlayerField.COINAGE,        stats.coinage)

    @staticmethod
    def get_object_fields(player, char_data):
        char_data.guid    = player.get(ObjectField.GUID)
        char_data.scale_x = player.get(ObjectField.SCALE_X)

    @staticmethod
    def get_unit_fields(player, char_data):
        stats = char_data.stats

        stats.health    = player.get(UnitField.HEALTH)
        stats.mana      = player.get(UnitField.POWER_1)
        stats.rage      = player.get(UnitField.POWER_2)
        stats.focus     = player.get(UnitField.POWER_3)
        stats.energy    = player.get(UnitField.POWER_4)
        stats.happiness = player.get(UnitField.POWER_5)

        stats.max_health    = player.get(UnitField.MAX_HEALTH)
        stats.max_mana      = player.get(UnitField.MAX_POWER_1)
        stats.max_rage      = player.get(UnitField.MAX_POWER_2)
        stats.max_focus     = player.get(UnitField.MAX_POWER_3)
        stats.max_energy    = player.get(UnitField.MAX_POWER_4)
        stats.max_happiness = player.get(UnitField.MAX_POWER_5)

        stats.level            = player.get(UnitField.LEVEL)
        stats.faction_template = player.get(UnitField.FACTION_TEMPLATE)
        unit_bytes_0           = player.get(UnitField.BYTES_0)
        char_data.race         = unit_bytes_0       & 0xFF
        char_data.class_id     = unit_bytes_0 >> 8  & 0xFF
        char_data.gender       = unit_bytes_0 >> 16 & 0xFF
        stats.unit_flags       = player.get(UnitField.FLAGS)

        stats.attack_time_mainhand = player.get(UnitField.BASE_ATTACK_TIME)
        stats.attack_time_offhand  = player.get(UnitField.OFFHAND_ATTACK_TIME)

        stats.bounding_radius = player.get(UnitField.BOUNDING_RADIUS)
        stats.combat_reach    = player.get(UnitField.COMBAT_REACH)

        stats.display_id        = player.get(UnitField.DISPLAY_ID)
        stats.native_display_id = player.get(UnitField.NATIVE_DISPLAY_ID)
        stats.mount_display_id  = player.get(UnitField.MOUNT_DISPLAY_ID)

        stats.min_damage         = player.get(UnitField.MIN_DAMAGE)
        stats.max_damage         = player.get(UnitField.MAX_DAMAGE)
        stats.min_offhand_damage = player.get(UnitField.MIN_OFFHAND_DAMAGE)
        stats.max_offhand_damage = player.get(UnitField.MAX_OFFHAND_DAMAGE)

        stats.unit_bytes_1 = player.get(UnitField.BYTES_1)

        stats.mod_cast_speed = player.get(UnitField.MOD_CAST_SPEED)

        stats.strength     = player.get(UnitField.STAT_0)
        stats.agility      = player.get(UnitField.STAT_1)
        stats.stamina      = player.get(UnitField.STAT_2)
        stats.intellect    = player.get(UnitField.STAT_3)
        stats.spirit       = player.get(UnitField.STAT_4)
        stats.resistance_0 = player.get(UnitField.RESISTANCE_0)
        stats.resistance_1 = player.get(UnitField.RESISTANCE_1)
        stats.resistance_2 = player.get(UnitField.RESISTANCE_2)
        stats.resistance_3 = player.get(UnitField.RESISTANCE_3)
        stats.resistance_4 = player.get(UnitField.RESISTANCE_4)
        stats.resistance_5 = player.get(UnitField.RESISTANCE_5)
        stats.resistance_6 = player.get(UnitField.RESISTANCE_6)

        stats.attack_power      = player.get(UnitField.ATTACK_POWER)
        stats.base_mana         = player.get(UnitField.BASE_MANA)
        stats.attack_power_mods = player.get(UnitField.ATTACK_POWER_MODS)

        stats.unit_bytes_2 = player.get(UnitField.BYTES_2)

        stats.ranged_attack_power = \
            player.get(UnitField.RANGED_ATTACK_POWER)
        stats.ranged_attack_power_mods = \
            player.get(UnitField.RANGED_ATTACK_POWER_MODS)

        stats.min_ranged_damage = player.get(UnitField.MIN_RANGED_DAMAGE)
        stats.max_ranged_damage = player.get(UnitField.MAX_RANGED_DAMAGE)

    @staticmethod
    def get_player_fields(player, char_data):
        stats = char_data.stats
        features = char_data.features

        stats.player_flags = player.get(PlayerField.FLAGS)

        player_bytes_1       = player.get(PlayerField.BYTES_1)
        features.skin        = player_bytes_1       & 0xFF
        features.face        = player_bytes_1 >> 8  & 0xFF
        features.hair_style  = player_bytes_1 >> 16 & 0xFF
        features.hair_color  = player_bytes_1 >> 24 & 0xFF
        player_bytes_2       = player.get(PlayerField.BYTES_2)
        features.facial_hair = player_bytes_2       & 0xFF
        stats.rest_info      = player_bytes_2 >> 24 & 0xFF
        player_bytes_3       = player.get(PlayerField.BYTES_3)
        char_data.gender     = player_bytes_3 & 0xFF

        stats.exp            = player.get(PlayerField.EXP)
        stats.next_level_exp = player.get(PlayerField.NEXT_LEVEL_EXP)

        stats.character_points_1 = player.get(PlayerField.CHARACTER_POINTS_1)
        stats.character_points_2 = player.get(PlayerField.CHARACTER_POINTS_2)

        stats.block_percentage = player.get(PlayerField.BLOCK_PERCENTAGE)
        stats.dodge_percentage = player.get(PlayerField.DODGE_PERCENTAGE)
        stats.parry_percentage = player.get(PlayerField.PARRY_PERCENTAGE)
        stats.crit_percentage  = player.get(PlayerField.CRIT_PERCENTAGE)

        stats.rest_state_exp = player.get(PlayerField.REST_STATE_EXP)
        stats.coinage        = player.get(PlayerField.COINAGE)
