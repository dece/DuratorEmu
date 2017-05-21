from durator.world.game.object.object_fields import (
    ObjectField, UnitField, PlayerField )
from durator.world.game.object.type.player import Player
from durator.world.game.update_object_packet import (
    UpdateType, UpdateObjectPacket )
from durator.common.log import LOG


# These values are enough to let the client make the player show in world.
# There may be a lot of superfluous values but well...
PLAYER_SPAWN_FIELDS = [
    ObjectField.GUID,
    ObjectField.TYPE,
    ObjectField.SCALE_X,
    UnitField.HEALTH,
    UnitField.POWER_1,
    UnitField.POWER_2,
    UnitField.POWER_3,
    UnitField.POWER_4,
    UnitField.POWER_5,
    UnitField.MAX_HEALTH,
    UnitField.MAX_POWER_1,
    UnitField.MAX_POWER_2,
    UnitField.MAX_POWER_3,
    UnitField.MAX_POWER_4,
    UnitField.MAX_POWER_5,
    UnitField.LEVEL,
    UnitField.FACTION_TEMPLATE,
    UnitField.BYTES_0,
    UnitField.FLAGS,
    UnitField.BASE_ATTACK_TIME,
    UnitField.OFFHAND_ATTACK_TIME,
    UnitField.BOUNDING_RADIUS,
    UnitField.COMBAT_REACH,
    UnitField.DISPLAY_ID,
    UnitField.NATIVE_DISPLAY_ID,
    UnitField.MOUNT_DISPLAY_ID,
    UnitField.MIN_DAMAGE,
    UnitField.MAX_DAMAGE,
    UnitField.MIN_OFFHAND_DAMAGE,
    UnitField.MAX_OFFHAND_DAMAGE,
    UnitField.BYTES_1,
    UnitField.MOD_CAST_SPEED,
    UnitField.STAT_0,
    UnitField.STAT_1,
    UnitField.STAT_2,
    UnitField.STAT_3,
    UnitField.STAT_4,
    UnitField.RESISTANCE_0,
    UnitField.RESISTANCE_1,
    UnitField.RESISTANCE_2,
    UnitField.RESISTANCE_3,
    UnitField.RESISTANCE_4,
    UnitField.RESISTANCE_5,
    UnitField.BASE_MANA,
    UnitField.BYTES_2,
    UnitField.ATTACK_POWER,
    UnitField.ATTACK_POWER_MODS,
    UnitField.RANGED_ATTACK_POWER,
    UnitField.RANGED_ATTACK_POWER_MODS,
    UnitField.MIN_RANGED_DAMAGE,
    UnitField.MAX_RANGED_DAMAGE,
    PlayerField.FLAGS,
    PlayerField.BYTES_1,
    PlayerField.BYTES_2,
    PlayerField.BYTES_3,
    PlayerField.EXP,
    PlayerField.NEXT_LEVEL_EXP,
    PlayerField.CHARACTER_POINTS_1,
    PlayerField.CHARACTER_POINTS_2,
    PlayerField.BLOCK_PERCENTAGE,
    PlayerField.DODGE_PERCENTAGE,
    PlayerField.PARRY_PERCENTAGE,
    PlayerField.CRIT_PERCENTAGE,
    PlayerField.REST_STATE_EXP,
    PlayerField.COINAGE
]


class PlayerSpawnPacket(UpdateObjectPacket):
    """ This specific UpdateObjectPacket is used to let a player spawn.
    Basically a wrapper around CREATE_OBJECT UpdateObjectPacket for Players that
    add some required fields. """

    def __init__(self, update_infos):
        super().__init__(UpdateType.CREATE_OBJECT, update_infos)

        player = update_infos["object"]
        with player.lock:
            self._add_required_fields(player)
            self._add_int_fields(player)

    def _add_required_fields(self, player):
        for required_field in PLAYER_SPAWN_FIELDS:
            value = player.get(required_field)
            if value is None:
                LOG.error("A required field for player spawning is not set.")
                LOG.error(str(required_field))
                continue
            self.add_field(required_field, value)

    def _add_int_fields(self, player):
        start_field = PlayerField.SKILL_INFO_1_ID.value
        for index in range(Player.NUM_SKILLS):
            field_value = start_field + index*3

            ident = player.get(field_value)
            if ident is None or ident == 0:
                continue
            else:
                self.add_field(field_value, ident)

            field_value += 1
            level = player.get(field_value)
            if level:
                self.add_field(field_value, level)

            field_value += 1
            stat_level = player.get(field_value)
            if stat_level:
                self.add_field(field_value, stat_level)
