""" Map all used update fields to an update type. """

from enum import Enum

from durator.world.game.object.object_fields import (
    ObjectField, ItemField, ContainerField,
    UnitField, PlayerField,
    DynamicObjectField, GameObjectField, CorpseField )
from durator.world.game.object.type.player import Player


class FieldType(Enum):

    INT32      = 1
    TWO_INT16  = 2
    FLOAT      = 3
    INT64      = 4
    FOUR_BYTES = 5


FIELD_TYPE_MAP = {

    # --------------------
    # Object fields
    # --------------------

    ObjectField.GUID:    FieldType.INT64,
    ObjectField.TYPE:    FieldType.INT32,
    ObjectField.ENTRY:   FieldType.INT32,
    ObjectField.SCALE_X: FieldType.FLOAT,

    # --------------------
    # Item fields
    # --------------------

    ItemField.OWNER:                FieldType.INT64,
    ItemField.CONTAINED:            FieldType.INT64,
    ItemField.CREATOR:              FieldType.INT64,
    ItemField.GIFTCREATOR:          FieldType.INT64,

    ItemField.STACK_COUNT:          FieldType.INT32,
    ItemField.DURATION:             FieldType.INT32,
    ItemField.SPELL_CHARGES:        FieldType.INT32,

    ItemField.FLAGS:                FieldType.TWO_INT16,

    ItemField.ENCHANTMENT:          FieldType.INT32,

    ItemField.PROPERTY_SEED:        FieldType.INT32,
    ItemField.RANDOM_PROPERTIES_ID: FieldType.INT32,
    ItemField.ITEM_TEXT_ID:         FieldType.INT32,

    ItemField.DURABILITY:           FieldType.INT32,
    ItemField.MAX_DURABILITY:       FieldType.INT32,

    # --------------------
    # Container fields
    # --------------------

    ContainerField.NUM_SLOTS: FieldType.INT32,
    ContainerField.SLOT_1:    FieldType.INT64,

    # --------------------
    # Unit fields
    # --------------------

    UnitField.CHARM:                     FieldType.INT64,
    UnitField.SUMMON:                    FieldType.INT64,
    UnitField.CHARMED_BY:                FieldType.INT64,
    UnitField.SUMMONED_BY:               FieldType.INT64,
    UnitField.CREATED_BY:                FieldType.INT64,
    UnitField.TARGET:                    FieldType.INT64,
    UnitField.PERSUADED:                 FieldType.INT64,
    UnitField.CHANNEL_OBJECT:            FieldType.INT64,

    UnitField.HEALTH:                    FieldType.INT32,
    UnitField.POWER_1:                   FieldType.INT32,
    UnitField.POWER_2:                   FieldType.INT32,
    UnitField.POWER_3:                   FieldType.INT32,
    UnitField.POWER_4:                   FieldType.INT32,
    UnitField.POWER_5:                   FieldType.INT32,

    UnitField.MAX_HEALTH:                FieldType.INT32,
    UnitField.MAX_POWER_1:               FieldType.INT32,
    UnitField.MAX_POWER_2:               FieldType.INT32,
    UnitField.MAX_POWER_3:               FieldType.INT32,
    UnitField.MAX_POWER_4:               FieldType.INT32,
    UnitField.MAX_POWER_5:               FieldType.INT32,

    UnitField.LEVEL:                     FieldType.INT32,
    UnitField.FACTION_TEMPLATE:          FieldType.INT32,
    UnitField.BYTES_0:                   FieldType.FOUR_BYTES,
    UnitField.VIRTUAL_ITEM_SLOT_DISPLAY: FieldType.INT32,
    UnitField.VIRTUAL_ITEM_INFO:         FieldType.FOUR_BYTES,
    UnitField.FLAGS:                     FieldType.INT32,

    UnitField.AURA:                      FieldType.INT32,
    UnitField.AURA_LEVELS:               FieldType.FOUR_BYTES,
    UnitField.AURA_APPLICATIONS:         FieldType.FOUR_BYTES,
    UnitField.AURA_FLAGS:                FieldType.FOUR_BYTES,
    UnitField.AURA_STATE:                FieldType.INT32,

    UnitField.BASE_ATTACK_TIME:          FieldType.INT32,
    UnitField.OFFHAND_ATTACK_TIME:       FieldType.INT32,
    UnitField.RANGED_ATTACK_TIME:        FieldType.INT32,

    UnitField.BOUNDING_RADIUS:           FieldType.FLOAT,
    UnitField.COMBAT_REACH:              FieldType.FLOAT,

    UnitField.DISPLAY_ID:                FieldType.INT32,
    UnitField.NATIVE_DISPLAY_ID:         FieldType.INT32,
    UnitField.MOUNT_DISPLAY_ID:          FieldType.INT32,

    UnitField.MIN_DAMAGE:                FieldType.FLOAT,
    UnitField.MAX_DAMAGE:                FieldType.FLOAT,
    UnitField.MIN_OFFHAND_DAMAGE:        FieldType.FLOAT,
    UnitField.MAX_OFFHAND_DAMAGE:        FieldType.FLOAT,

    UnitField.BYTES_1:                   FieldType.FOUR_BYTES,

    UnitField.PET_NUMBER:                FieldType.INT32,
    UnitField.PET_NAME_TIMESTAMP:        FieldType.INT32,
    UnitField.PET_EXPERIENCE:            FieldType.INT32,
    UnitField.PET_NEXT_LEVEL_EXP:        FieldType.INT32,

    UnitField.DYNAMIC_FLAGS:             FieldType.INT32,
    UnitField.CHANNEL_SPELL:             FieldType.INT32,
    UnitField.MOD_CAST_SPEED:            FieldType.INT32,
    UnitField.CREATED_BY_SPELL:          FieldType.INT32,

    UnitField.NPC_FLAGS:                 FieldType.INT32,
    UnitField.NPC_EMOTESTATE:            FieldType.INT32,

    UnitField.TRAINING_POINTS:           FieldType.TWO_INT16,

    UnitField.STAT_0:                    FieldType.INT32,
    UnitField.STAT_1:                    FieldType.INT32,
    UnitField.STAT_2:                    FieldType.INT32,
    UnitField.STAT_3:                    FieldType.INT32,
    UnitField.STAT_4:                    FieldType.INT32,
    UnitField.RESISTANCE_0:              FieldType.INT32,
    UnitField.RESISTANCE_1:              FieldType.INT32,
    UnitField.RESISTANCE_2:              FieldType.INT32,
    UnitField.RESISTANCE_3:              FieldType.INT32,
    UnitField.RESISTANCE_4:              FieldType.INT32,
    UnitField.RESISTANCE_5:              FieldType.INT32,
    UnitField.RESISTANCE_6:              FieldType.INT32,

    UnitField.ATTACK_POWER:              FieldType.INT32,
    UnitField.BASE_MANA:                 FieldType.INT32,
    UnitField.ATTACK_POWER_MODS:         FieldType.TWO_INT16,

    UnitField.BYTES_2:                   FieldType.FOUR_BYTES,

    UnitField.RANGED_ATTACK_POWER:       FieldType.INT32,
    UnitField.RANGED_ATTACK_POWER_MODS:  FieldType.TWO_INT16,
    UnitField.MIN_RANGED_DAMAGE:         FieldType.FLOAT,
    UnitField.MAX_RANGED_DAMAGE:         FieldType.FLOAT,

    # --------------------
    # Player fields
    # --------------------

    PlayerField.SELECTION:                 FieldType.INT64,
    PlayerField.DUEL_ARBITER:              FieldType.INT64,
    PlayerField.FLAGS:                     FieldType.INT32,

    PlayerField.GUILD_ID:                  FieldType.INT32,
    PlayerField.GUILD_RANK:                FieldType.INT32,

    PlayerField.BYTES_1:                   FieldType.FOUR_BYTES,
    PlayerField.BYTES_2:                   FieldType.FOUR_BYTES,
    PlayerField.BYTES_3:                   FieldType.FOUR_BYTES,

    PlayerField.DUEL_TEAM:                 FieldType.INT32,
    PlayerField.GUILD_TIMESTAMP:           FieldType.INT32,

    PlayerField.INV_SLOT_HEAD:             FieldType.INT64,

    PlayerField.PACK_SLOT_1:               FieldType.INT64,

    PlayerField.BANK_SLOT_1:               FieldType.INT64,

    PlayerField.BANK_BAG_SLOT_1:           FieldType.INT64,

    PlayerField.VENDOR_BUY_BACK_SLOT:      FieldType.INT64,

    PlayerField.FAR_SIGHT:                 FieldType.INT64,
    PlayerField.COMBO_TARGET:              FieldType.INT64,

    PlayerField.BUY_BACK_NPC:              FieldType.INT64,

    PlayerField.EXP:                       FieldType.INT32,
    PlayerField.NEXT_LEVEL_EXP:            FieldType.INT32,

    PlayerField.QUEST_LOG_1_1:             FieldType.INT32,
    PlayerField.QUEST_LOG_1_2:             FieldType.INT32,
    PlayerField.QUEST_LOG_1_3:             FieldType.INT32,

    PlayerField.CHARACTER_POINTS_1:        FieldType.INT32,
    PlayerField.CHARACTER_POINTS_2:        FieldType.INT32,

    PlayerField.TRACK_CREATURES:           FieldType.INT32,
    PlayerField.TRACK_RESOURCES:           FieldType.INT32,

    PlayerField.CHAT_FILTERS:              FieldType.INT32,

    PlayerField.BLOCK_PERCENTAGE:          FieldType.FLOAT,
    PlayerField.DODGE_PERCENTAGE:          FieldType.FLOAT,
    PlayerField.PARRY_PERCENTAGE:          FieldType.FLOAT,
    PlayerField.CRIT_PERCENTAGE:           FieldType.FLOAT,

    PlayerField.EXPLORED_ZONES_1:          FieldType.FOUR_BYTES,

    PlayerField.REST_STATE_EXP:            FieldType.INT32,
    PlayerField.COINAGE:                   FieldType.INT32,

    PlayerField.POS_STAT_0:                FieldType.INT32,
    PlayerField.POS_STAT_1:                FieldType.INT32,
    PlayerField.POS_STAT_2:                FieldType.INT32,
    PlayerField.POS_STAT_3:                FieldType.INT32,
    PlayerField.POS_STAT_4:                FieldType.INT32,
    PlayerField.NEG_STAT_0:                FieldType.INT32,
    PlayerField.NEG_STAT_1:                FieldType.INT32,
    PlayerField.NEG_STAT_2:                FieldType.INT32,
    PlayerField.NEG_STAT_3:                FieldType.INT32,
    PlayerField.NEG_STAT_4:                FieldType.INT32,

    PlayerField.RESISTANCE_0_BUFF_MOD_POS: FieldType.INT32,
    PlayerField.RESISTANCE_1_BUFF_MOD_POS: FieldType.INT32,
    PlayerField.RESISTANCE_2_BUFF_MOD_POS: FieldType.INT32,
    PlayerField.RESISTANCE_3_BUFF_MOD_POS: FieldType.INT32,
    PlayerField.RESISTANCE_4_BUFF_MOD_POS: FieldType.INT32,
    PlayerField.RESISTANCE_5_BUFF_MOD_POS: FieldType.INT32,
    PlayerField.RESISTANCE_6_BUFF_MOD_POS: FieldType.INT32,
    PlayerField.RESISTANCE_0_BUFF_MOD_NEG: FieldType.INT32,
    PlayerField.RESISTANCE_1_BUFF_MOD_NEG: FieldType.INT32,
    PlayerField.RESISTANCE_2_BUFF_MOD_NEG: FieldType.INT32,
    PlayerField.RESISTANCE_3_BUFF_MOD_NEG: FieldType.INT32,
    PlayerField.RESISTANCE_4_BUFF_MOD_NEG: FieldType.INT32,
    PlayerField.RESISTANCE_5_BUFF_MOD_NEG: FieldType.INT32,
    PlayerField.RESISTANCE_6_BUFF_MOD_NEG: FieldType.INT32,

    PlayerField.MOD_DAMAGE_0_DONE_POS:     FieldType.INT32,
    PlayerField.MOD_DAMAGE_1_DONE_POS:     FieldType.INT32,
    PlayerField.MOD_DAMAGE_2_DONE_POS:     FieldType.INT32,
    PlayerField.MOD_DAMAGE_3_DONE_POS:     FieldType.INT32,
    PlayerField.MOD_DAMAGE_4_DONE_POS:     FieldType.INT32,
    PlayerField.MOD_DAMAGE_5_DONE_POS:     FieldType.INT32,
    PlayerField.MOD_DAMAGE_6_DONE_POS:     FieldType.INT32,
    PlayerField.MOD_DAMAGE_0_DONE_NEG:     FieldType.INT32,
    PlayerField.MOD_DAMAGE_1_DONE_NEG:     FieldType.INT32,
    PlayerField.MOD_DAMAGE_2_DONE_NEG:     FieldType.INT32,
    PlayerField.MOD_DAMAGE_3_DONE_NEG:     FieldType.INT32,
    PlayerField.MOD_DAMAGE_4_DONE_NEG:     FieldType.INT32,
    PlayerField.MOD_DAMAGE_5_DONE_NEG:     FieldType.INT32,
    PlayerField.MOD_DAMAGE_6_DONE_NEG:     FieldType.INT32,
    PlayerField.MOD_DAMAGE_0_DONE_PCT:     FieldType.INT32,
    PlayerField.MOD_DAMAGE_1_DONE_PCT:     FieldType.INT32,
    PlayerField.MOD_DAMAGE_2_DONE_PCT:     FieldType.INT32,
    PlayerField.MOD_DAMAGE_3_DONE_PCT:     FieldType.INT32,
    PlayerField.MOD_DAMAGE_4_DONE_PCT:     FieldType.INT32,
    PlayerField.MOD_DAMAGE_5_DONE_PCT:     FieldType.INT32,
    PlayerField.MOD_DAMAGE_6_DONE_PCT:     FieldType.INT32,

    PlayerField.BYTES_4:                   FieldType.FOUR_BYTES,

    PlayerField.AMMO_ID:                   FieldType.INT32,

    PlayerField.PVP_MEDALS:                FieldType.INT32,

    PlayerField.BUYBACK_ITEM_ID:           FieldType.INT32,
    PlayerField.BUYBACK_RANDOM_PROP_ID:    FieldType.INT32,
    PlayerField.BUYBACK_SEED:              FieldType.INT32,
    PlayerField.BUYBACK_PRICE:             FieldType.INT32,

    # --------------------
    # Game object fields
    # --------------------

    GameObjectField.DISPLAY_ID: FieldType.INT32,
    GameObjectField.FLAGS:      FieldType.INT32,

    GameObjectField.ROTATION_1: FieldType.FLOAT,
    GameObjectField.ROTATION_2: FieldType.FLOAT,
    GameObjectField.ROTATION_3: FieldType.FLOAT,
    GameObjectField.ROTATION_4: FieldType.FLOAT,

    GameObjectField.STATE:      FieldType.INT32,
    GameObjectField.TIMESTAMP:  FieldType.INT32,

    GameObjectField.POS_X:      FieldType.FLOAT,
    GameObjectField.POS_Y:      FieldType.FLOAT,
    GameObjectField.POS_Z:      FieldType.FLOAT,
    GameObjectField.FACING:     FieldType.FLOAT,

    GameObjectField.DYN_FLAGS:  FieldType.INT32,
    GameObjectField.FACTION:    FieldType.INT32,
    GameObjectField.TYPE_ID:    FieldType.INT32,
    GameObjectField.LEVEL:      FieldType.INT32,

    # --------------------
    # Dynamic object fields
    # --------------------

    DynamicObjectField.CASTER:   FieldType.INT64,
    DynamicObjectField.BYTES:    FieldType.FOUR_BYTES,
    DynamicObjectField.SPELL_ID: FieldType.INT32,
    DynamicObjectField.RADIUS:   FieldType.FLOAT,

    DynamicObjectField.POS_X:    FieldType.FLOAT,
    DynamicObjectField.POS_Y:    FieldType.FLOAT,
    DynamicObjectField.POS_Z:    FieldType.FLOAT,
    DynamicObjectField.FACING:   FieldType.FLOAT,

    # --------------------
    # Corpse fields
    # --------------------

    CorpseField.OWNER:      FieldType.INT64,

    CorpseField.FACING:     FieldType.FLOAT,
    CorpseField.POS_X:      FieldType.FLOAT,
    CorpseField.POS_Y:      FieldType.FLOAT,
    CorpseField.POS_Z:      FieldType.FLOAT,

    CorpseField.DISPLAY_ID: FieldType.INT32,

    CorpseField.ITEM_1:     FieldType.INT32,

    CorpseField.BYTES_1:    FieldType.FOUR_BYTES,
    CorpseField.BYTES_2:    FieldType.FOUR_BYTES,

    CorpseField.GUILD:      FieldType.INT32,
    CorpseField.FLAGS:      FieldType.INT32

}


for i in range(Player.NUM_SKILLS):
    FIELD_TYPE_MAP.update({
        PlayerField.SKILL_INFO_1_ID.value + i*3:         FieldType.INT32,
        PlayerField.SKILL_INFO_1_LEVEL.value + i*3:      FieldType.INT32,
        PlayerField.SKILL_INFO_1_STAT_LEVEL.value + i*3: FieldType.INT32
    })
