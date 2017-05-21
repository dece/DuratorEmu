from abc import ABCMeta
import threading

from peewee import PeeweeException

from durator.config import CONFIG
from durator.db.database import DB, db_connection
from durator.world.game.character.manager import CharacterManager
from durator.world.game.object.object_fields import (
    ObjectField, UnitField, PlayerField )
from durator.world.game.object.type.base_object import (
    ObjectType, OBJECT_TYPE_TO_FLAGS )
from durator.world.game.object.type.player import Player
from durator.world.game.player_spawn_packet import PlayerSpawnPacket
from durator.world.game.update_object_packet import (
    UpdateType, UpdateObjectPacket )
from durator.world.world_connection_state import WorldConnectionState
from durator.common.log import LOG


def lock(func):
    def lock_decorator(self, *args, **kwargs):
        with self.lock:
            return func(self, *args, **kwargs)
    return lock_decorator


class BaseObjectManager(metaclass = ABCMeta):
    """ All objects manager for any kind of game object inherit from this.
    A BaseObjectManager has an access to the server to easily pass messages. """

    def __init__(self, server):
        self.server = server
        self.objects = {}
        self.lock = threading.RLock()  # temporary fix, should be a Lock

    @lock
    def _add_object(self, misc_object):
        self.objects[misc_object.guid] = misc_object

    @lock
    def _get_object(self, guid):
        return self.objects.get(guid)

    @lock
    def _get_guids(self):
        return list(self.objects.keys())

    @lock
    def _remove_object(self, guid):
        del self.objects[guid]





class ObjectManager(BaseObjectManager):
    """ Manage all objects in world. To avoid an overcrowded class, boring
    stuff is moved to friend classes. """

    def __init__(self, server):
        super().__init__(server)
        self.player_manager = _PlayerManager(server)

    # ----------------------------------------
    # Add diverse objects to the world
    # ----------------------------------------

    def add_player(self, char_data):
        """ Create (and return) a Player object from the data stored in the
        database, and add it to the managed object list. """
        return self.player_manager.create_player(char_data)

    @staticmethod
    def add_object_coords(base_object, position_data):
        """ Import position data from database to this BaseObject. """
        with base_object.lock:
            base_object.map_id     = position_data.map_id
            base_object.zone_id    = position_data.zone_id
            base_object.position.x = position_data.pos_x
            base_object.position.y = position_data.pos_y
            base_object.position.z = position_data.pos_z
            base_object.position.o = position_data.orientation

    @staticmethod
    @db_connection
    def add_object_fields(base_object, object_data, object_type):
        """ Import BaseObject data mostly from database to this object. """
        with base_object.lock:
            base_object.set(ObjectField.GUID,    object_data.guid)
            base_object.set(ObjectField.TYPE,    object_type)
            base_object.set(ObjectField.SCALE_X, object_data.stats.scale_x)

    # ----------------------------------------
    # Access diverse objects' data from the world
    # ----------------------------------------

    def get_player(self, guid):
        """ Return the player with that GUID, or None if it doesn't exist. """
        return self.player_manager.get_player(guid)

    def get_player_guids(self):
        """ Return an iterable over registered Player GUIDs. """
        return self.player_manager.get_guids()

    def players_in_range_of(self, player, dist_range):
        return self.player_manager.players_in_range_of(player, dist_range)

    # ----------------------------------------
    # Modify objects in the world
    # ----------------------------------------

    def save_player(self, player):
        """ Save the Player to the database. """
        self.player_manager.save_player(player)

    def update_movement(self, ref_player):
        """ Send ref_player update movement packets to near players. """
        ref_guid = ref_player.guid
        dist_range = float(CONFIG["world"]["update_range"])
        players_guids = self.players_in_range_of(ref_player, dist_range)

        update_movement_guids, update_create_guids = \
            self._tracking_and_untracking_players(
                ref_guid,
                players_guids,
                update = True
            )

        infos = { "object": ref_player, "is_player": False }
        create_packet = PlayerSpawnPacket(infos)
        movement_packet = UpdateObjectPacket(UpdateType.MOVEMENT, infos)

        # If a player is not tracking our reference player (= it doesn't
        # know about that GUID), send a create object packet.
        self.server.broadcast(
            create_packet,
            state = WorldConnectionState.IN_WORLD,
            guids = update_create_guids
        )

        # Else (already tracking ref_player), send a movement update.
        self.server.broadcast(
            movement_packet,
            state = WorldConnectionState.IN_WORLD,
            guids = update_movement_guids
        )

    def _tracking_and_untracking_players(self, ref_guid, players_guids,
            update = False):
        """ Return lists of players (from the GUID list) that are tracking or
        not tracking ref_player. If update is True, append ref_guid to all not
        previously tracking players. """
        tracking_guids = []
        not_tracking_guids = []

        for player in [self.get_player(guid) for guid in players_guids]:
            if player is None:
                continue
            with player.lock:
                if ref_guid not in player.tracked_guids:
                    not_tracking_guids.append(player.guid)
                    if update:
                        player.tracked_guids.append(ref_guid)
                else:
                    tracking_guids.append(player.guid)

        return tracking_guids, not_tracking_guids

    # ----------------------------------------
    # Remove diverse objects from the world
    # ----------------------------------------

    def remove_player(self, guid):
        """ Remove the player from the object list and save its data. """
        self.player_manager.remove_player(guid)

    @staticmethod
    def save_object_coords(base_object, position):
        """ Save BaseObject's position data into the database. """
        with base_object.lock:
            position.map_id      = base_object.map_id
            position.zone_id     = base_object.zone_id
            position.pos_x       = base_object.position.x
            position.pos_y       = base_object.position.y
            position.pos_z       = base_object.position.z
            position.orientation = base_object.position.o
        position.save()

    @staticmethod
    @db_connection
    def save_object_fields(base_object, base_object_data):
        """ Save the BaseObject's fields into the database. """
        with base_object.lock:
            base_object_data.guid    = base_object.get(ObjectField.GUID)
            base_object_data.scale_x = base_object.get(ObjectField.SCALE_X)
        base_object_data.save()





class _UnitManager(BaseObjectManager):

    def __init__(self, server):
        super().__init__(server)

    @staticmethod
    @db_connection
    def add_unit_fields(unit, unit_data):
        """ Import into this Unit field values from the database. """
        with unit.lock:
            stats = unit_data.stats

            unit.set(UnitField.HEALTH,  stats.health)
            unit.set(UnitField.POWER_1, stats.mana)
            unit.set(UnitField.POWER_2, stats.rage)
            unit.set(UnitField.POWER_3, stats.focus)
            unit.set(UnitField.POWER_4, stats.energy)
            unit.set(UnitField.POWER_5, stats.happiness)

            unit.set(UnitField.MAX_HEALTH,  stats.max_health)
            unit.set(UnitField.MAX_POWER_1, stats.max_mana)
            unit.set(UnitField.MAX_POWER_2, stats.max_rage)
            unit.set(UnitField.MAX_POWER_3, stats.max_focus)
            unit.set(UnitField.MAX_POWER_4, stats.max_energy)
            unit.set(UnitField.MAX_POWER_5, stats.max_happiness)

            unit_bytes_0 = (
                unit_data.race          |
                unit_data.class_id << 8 |
                unit_data.gender << 16  |
                1 << 24
            )

            unit.set(UnitField.LEVEL,            stats.level)
            unit.set(UnitField.FACTION_TEMPLATE, stats.faction_template)
            unit.set(UnitField.BYTES_0,          unit_bytes_0)
            unit.set(UnitField.FLAGS,            stats.unit_flags)

            unit.set(UnitField.BASE_ATTACK_TIME,    stats.attack_time_mainhand)
            unit.set(UnitField.OFFHAND_ATTACK_TIME, stats.attack_time_offhand)

            unit.set(UnitField.BOUNDING_RADIUS, stats.bounding_radius)
            unit.set(UnitField.COMBAT_REACH,    stats.combat_reach)

            unit.set(UnitField.DISPLAY_ID,        stats.display_id)
            unit.set(UnitField.NATIVE_DISPLAY_ID, stats.native_display_id)
            unit.set(UnitField.MOUNT_DISPLAY_ID,  stats.mount_display_id)

            unit.set(UnitField.MIN_DAMAGE,         stats.min_damage)
            unit.set(UnitField.MAX_DAMAGE,         stats.max_damage)
            unit.set(UnitField.MIN_OFFHAND_DAMAGE, stats.min_offhand_damage)
            unit.set(UnitField.MAX_OFFHAND_DAMAGE, stats.max_offhand_damage)

            unit.set(UnitField.BYTES_1, stats.unit_bytes_1)

            unit.set(UnitField.MOD_CAST_SPEED, stats.mod_cast_speed)

            unit.set(UnitField.STAT_0,       stats.strength)
            unit.set(UnitField.STAT_1,       stats.agility)
            unit.set(UnitField.STAT_2,       stats.stamina)
            unit.set(UnitField.STAT_3,       stats.intellect)
            unit.set(UnitField.STAT_4,       stats.spirit)
            unit.set(UnitField.RESISTANCE_0, stats.resistance_0)
            unit.set(UnitField.RESISTANCE_1, stats.resistance_1)
            unit.set(UnitField.RESISTANCE_2, stats.resistance_2)
            unit.set(UnitField.RESISTANCE_3, stats.resistance_3)
            unit.set(UnitField.RESISTANCE_4, stats.resistance_4)
            unit.set(UnitField.RESISTANCE_5, stats.resistance_5)
            unit.set(UnitField.RESISTANCE_6, stats.resistance_6)

            unit.set(UnitField.ATTACK_POWER,      stats.attack_power)
            unit.set(UnitField.BASE_MANA,         stats.base_mana)
            unit.set(UnitField.ATTACK_POWER_MODS, stats.attack_power_mods)

            unit.set(UnitField.BYTES_2, stats.unit_bytes_2)

            unit.set(UnitField.RANGED_ATTACK_POWER,
                stats.ranged_attack_power)
            unit.set(UnitField.RANGED_ATTACK_POWER_MODS,
                stats.ranged_attack_power_mods)
            unit.set(UnitField.MIN_RANGED_DAMAGE, stats.min_ranged_damage)
            unit.set(UnitField.MAX_RANGED_DAMAGE, stats.max_ranged_damage)

    @staticmethod
    @db_connection
    def save_unit_fields(unit, unit_data):
        """ Save Unit fields into the database. """
        with unit.lock:
            stats = unit_data.stats

            stats.health    = unit.get(UnitField.HEALTH)
            stats.mana      = unit.get(UnitField.POWER_1)
            stats.rage      = unit.get(UnitField.POWER_2)
            stats.focus     = unit.get(UnitField.POWER_3)
            stats.energy    = unit.get(UnitField.POWER_4)
            stats.happiness = unit.get(UnitField.POWER_5)

            stats.max_health    = unit.get(UnitField.MAX_HEALTH)
            stats.max_mana      = unit.get(UnitField.MAX_POWER_1)
            stats.max_rage      = unit.get(UnitField.MAX_POWER_2)
            stats.max_focus     = unit.get(UnitField.MAX_POWER_3)
            stats.max_energy    = unit.get(UnitField.MAX_POWER_4)
            stats.max_happiness = unit.get(UnitField.MAX_POWER_5)

            stats.level            = unit.get(UnitField.LEVEL)
            stats.faction_template = unit.get(UnitField.FACTION_TEMPLATE)
            unit_bytes_0           = unit.get(UnitField.BYTES_0)
            unit_data.race         = unit_bytes_0       & 0xFF
            unit_data.class_id     = unit_bytes_0 >> 8  & 0xFF
            unit_data.gender       = unit_bytes_0 >> 16 & 0xFF
            stats.unit_flags       = unit.get(UnitField.FLAGS)

            stats.attack_time_mainhand = unit.get(UnitField.BASE_ATTACK_TIME)
            stats.attack_time_offhand  = unit.get(UnitField.OFFHAND_ATTACK_TIME)

            stats.bounding_radius = unit.get(UnitField.BOUNDING_RADIUS)
            stats.combat_reach    = unit.get(UnitField.COMBAT_REACH)

            stats.display_id        = unit.get(UnitField.DISPLAY_ID)
            stats.native_display_id = unit.get(UnitField.NATIVE_DISPLAY_ID)
            stats.mount_display_id  = unit.get(UnitField.MOUNT_DISPLAY_ID)

            stats.min_damage         = unit.get(UnitField.MIN_DAMAGE)
            stats.max_damage         = unit.get(UnitField.MAX_DAMAGE)
            stats.min_offhand_damage = unit.get(UnitField.MIN_OFFHAND_DAMAGE)
            stats.max_offhand_damage = unit.get(UnitField.MAX_OFFHAND_DAMAGE)

            stats.unit_bytes_1 = unit.get(UnitField.BYTES_1)

            stats.mod_cast_speed = unit.get(UnitField.MOD_CAST_SPEED)

            stats.strength     = unit.get(UnitField.STAT_0)
            stats.agility      = unit.get(UnitField.STAT_1)
            stats.stamina      = unit.get(UnitField.STAT_2)
            stats.intellect    = unit.get(UnitField.STAT_3)
            stats.spirit       = unit.get(UnitField.STAT_4)
            stats.resistance_0 = unit.get(UnitField.RESISTANCE_0)
            stats.resistance_1 = unit.get(UnitField.RESISTANCE_1)
            stats.resistance_2 = unit.get(UnitField.RESISTANCE_2)
            stats.resistance_3 = unit.get(UnitField.RESISTANCE_3)
            stats.resistance_4 = unit.get(UnitField.RESISTANCE_4)
            stats.resistance_5 = unit.get(UnitField.RESISTANCE_5)
            stats.resistance_6 = unit.get(UnitField.RESISTANCE_6)

            stats.attack_power      = unit.get(UnitField.ATTACK_POWER)
            stats.base_mana         = unit.get(UnitField.BASE_MANA)
            stats.attack_power_mods = unit.get(UnitField.ATTACK_POWER_MODS)

            stats.unit_bytes_2 = unit.get(UnitField.BYTES_2)

            stats.ranged_attack_power = \
                unit.get(UnitField.RANGED_ATTACK_POWER)
            stats.ranged_attack_power_mods = \
                unit.get(UnitField.RANGED_ATTACK_POWER_MODS)

            stats.min_ranged_damage = unit.get(UnitField.MIN_RANGED_DAMAGE)
            stats.max_ranged_damage = unit.get(UnitField.MAX_RANGED_DAMAGE)

        stats.save()
        unit_data.save()





class _PlayerManager(BaseObjectManager):
    """ The player manager handles all player in world, but must be accessed
    from the more general object manager for now. """

    def __init__(self, server):
        super().__init__(server)

    # ----------------------------------------
    # Add players to world
    # ----------------------------------------

    @db_connection
    def create_player(self, char_data):
        """ Create a new Player object in world. """
        player = Player()
        player.name = char_data.name

        position = char_data.position
        object_type = OBJECT_TYPE_TO_FLAGS[ObjectType.PLAYER]

        ObjectManager.add_object_coords(player, position)
        player.movement.position = player.position
        ObjectManager.add_object_fields(player, char_data, object_type)
        _UnitManager.add_unit_fields(player, char_data)
        _PlayerManager.add_player_fields(player, char_data)
        player.import_skills(char_data)
        player.import_spells(char_data)

        self._add_object(player)
        return player

    @staticmethod
    @db_connection
    def add_player_fields(player, char_data):
        """ Import player database data into the player object. """
        with player.lock:
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

    # ----------------------------------------
    # Access players data
    # ----------------------------------------

    def get_player(self, guid):
        return self._get_object(guid)

    def get_guids(self):
        return self._get_guids()

    @lock
    def players_in_range_of(self, ref_player, dist_range):
        """ Return a list of Players' GUIDs in that ref_player's range."""
        with ref_player.lock:
            ref_position = ref_player.position

        guids_in_range = []
        for player_guid in self.objects:
            player = self.get_player(player_guid)
            if ref_position.distance_from(player.position) < dist_range:
                if ref_player.guid != player_guid:
                    guids_in_range.append(player_guid)
        return guids_in_range

    # ----------------------------------------
    # Remove players from world
    # ----------------------------------------

    def remove_player(self, guid):
        """ Remove the player from the object list and save its data. """
        player = self.get_player(guid)
        if player is None:
            LOG.warning("Tried to remove a non-existing player.")
            return

        self._remove_object(guid)
        self.save_player(player)

    @db_connection
    def save_player(self, player):
        char_data = CharacterManager.get_char_data(player.guid)

        with DB.atomic() as transaction:
            try:
                ObjectManager.save_object_coords(player, char_data.position)
                ObjectManager.save_object_fields(player, char_data)
                _UnitManager.save_unit_fields(player, char_data)
                _PlayerManager.save_player_fields(player, char_data)
                char_data.save()
            except PeeweeException as exc:
                LOG.error("An error occured while creating character:")
                LOG.error(str(exc))
                transaction.rollback()
                return None

    @staticmethod
    @db_connection
    def save_player_fields(player, char_data):
        """ Export player object data into the database. """
        with player.lock:
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

            stats.character_points_1 = \
                player.get(PlayerField.CHARACTER_POINTS_1)
            stats.character_points_2 = \
                player.get(PlayerField.CHARACTER_POINTS_2)

            stats.block_percentage = player.get(PlayerField.BLOCK_PERCENTAGE)
            stats.dodge_percentage = player.get(PlayerField.DODGE_PERCENTAGE)
            stats.parry_percentage = player.get(PlayerField.PARRY_PERCENTAGE)
            stats.crit_percentage  = player.get(PlayerField.CRIT_PERCENTAGE)

            stats.rest_state_exp = player.get(PlayerField.REST_STATE_EXP)
            stats.coinage        = player.get(PlayerField.COINAGE)

        features.save()
        stats.save()
        char_data.save()
