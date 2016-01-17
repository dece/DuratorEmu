from durator.world.game.object.base_object import ObjectDescFlags
from durator.world.game.object.object_fields import (
    ObjectField, UnitField, PlayerField )
from durator.world.game.object.player import Player


class ObjectManager(object):

    def __init__(self):
        self.players = {}

    def add_player(self, char_data):
        """ Create (and return) a Player object from the data stored in the
        database, and add it to the managed object list. """
        player = Player()
        player.name = char_data.name

        ObjectManager._add_coords_to_object(player, char_data.position)
        ObjectManager._add_object_fields_to_player(player, char_data)
        ObjectManager._add_unit_fields_to_player(player, char_data)
        ObjectManager._add_player_fields_to_player(player, char_data)

        guid = player.get(ObjectField.GUID)
        self.players[guid] = player
        return player

    @staticmethod
    def _add_coords_to_object(base_object, position_data):
        base_object.coords["map"] = position_data.map_id
        base_object.coords["zone"] = position_data.zone_id
        base_object.coords["x"] = position_data.pos_x
        base_object.coords["y"] = position_data.pos_y
        base_object.coords["z"] = position_data.pos_z
        base_object.coords["o"] = position_data.orientation

    @staticmethod
    def _add_object_fields_to_player(player, char_data):
        object_type = (
            ObjectDescFlags.OBJECT.value |
            ObjectDescFlags.UNIT.value   |
            ObjectDescFlags.PLAYER.value
        )
        player.set(ObjectField.GUID,    char_data.guid)
        player.set(ObjectField.TYPE,    object_type)
        player.set(ObjectField.SCALE_X, char_data.stats.scale_x)

    @staticmethod
    def _add_unit_fields_to_player(player, char_data):
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
    def _add_player_fields_to_player(player, char_data):
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

    def get(self, guid):
        """ Return the object with that GUID, or None if it doesn't exist. """
        return self.players.get(guid)


OBJECT_MANAGER = ObjectManager()
