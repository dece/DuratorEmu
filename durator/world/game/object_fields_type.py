""" Map all used update fields to an update type. """

from enum import Enum

from durator.world.game.object_fields import (
    FieldObject, FieldItem, FieldContainer,
    FieldUnit, FieldPlayer,
    FieldDynamicObject, FieldGameObject, FieldCorpse )


class FieldsType(Enum):

    INT32      = 1
    TWO_INT16  = 2
    FLOAT      = 3
    INT64      = 4
    FOUR_BYTES = 5


FIELD_TYPE_MAP = {

    # --------------------
    # Object fields
    # --------------------

    FieldObject.GUID:    FieldsType.INT64,
    FieldObject.TYPE:    FieldsType.INT32,
    FieldObject.ENTRY:   FieldsType.INT32,
    FieldObject.SCALE_X: FieldsType.FLOAT,

    # --------------------
    # Item fields
    # --------------------

    FieldItem.OWNER:                FieldsType.INT64,
    FieldItem.CONTAINED:            FieldsType.INT64,
    FieldItem.CREATOR:              FieldsType.INT64,
    FieldItem.GIFTCREATOR:          FieldsType.INT64,

    FieldItem.STACK_COUNT:          FieldsType.INT32,
    FieldItem.DURATION:             FieldsType.INT32,
    FieldItem.SPELL_CHARGES:        FieldsType.INT32,

    FieldItem.FLAGS:                FieldsType.TWO_INT16,

    FieldItem.ENCHANTMENT:          FieldsType.INT32,

    FieldItem.PROPERTY_SEED:        FieldsType.INT32,
    FieldItem.RANDOM_PROPERTIES_ID: FieldsType.INT32,
    FieldItem.ITEM_TEXT_ID:         FieldsType.INT32,

    FieldItem.DURABILITY:           FieldsType.INT32,
    FieldItem.MAX_DURABILITY:       FieldsType.INT32,

    # --------------------
    # Container fields
    # --------------------

    FieldContainer.NUM_SLOTS: FieldsType.INT32,
    FieldContainer.SLOT_1:    FieldsType.INT64,

    # --------------------
    # Unit fields
    # --------------------

    FieldUnit.CHARM:                     FieldsType.INT64,
    FieldUnit.SUMMON:                    FieldsType.INT64,
    FieldUnit.CHARMED_BY:                FieldsType.INT64,
    FieldUnit.SUMMONED_BY:               FieldsType.INT64,
    FieldUnit.CREATED_BY:                FieldsType.INT64,
    FieldUnit.TARGET:                    FieldsType.INT64,
    FieldUnit.PERSUADED:                 FieldsType.INT64,
    FieldUnit.CHANNEL_OBJECT:            FieldsType.INT64,

    FieldUnit.HEALTH:                    FieldsType.INT32,
    FieldUnit.POWER_1:                   FieldsType.INT32,
    FieldUnit.POWER_2:                   FieldsType.INT32,
    FieldUnit.POWER_3:                   FieldsType.INT32,
    FieldUnit.POWER_4:                   FieldsType.INT32,
    FieldUnit.POWER_5:                   FieldsType.INT32,

    FieldUnit.MAX_HEALTH:                FieldsType.INT32,
    FieldUnit.MAX_POWER_1:               FieldsType.INT32,
    FieldUnit.MAX_POWER_2:               FieldsType.INT32,
    FieldUnit.MAX_POWER_3:               FieldsType.INT32,
    FieldUnit.MAX_POWER_4:               FieldsType.INT32,
    FieldUnit.MAX_POWER_5:               FieldsType.INT32,

    FieldUnit.LEVEL:                     FieldsType.INT32,
    FieldUnit.FACTION_TEMPLATE:          FieldsType.INT32,
    FieldUnit.BYTES_0:                   FieldsType.FOUR_BYTES,
    FieldUnit.VIRTUAL_ITEM_SLOT_DISPLAY: FieldsType.INT32,
    FieldUnit.VIRTUAL_ITEM_INFO:         FieldsType.FOUR_BYTES,
    FieldUnit.FLAGS:                     FieldsType.INT32,

    FieldUnit.AURA:                      FieldsType.INT32,
    FieldUnit.AURA_LEVELS:               FieldsType.FOUR_BYTES,
    FieldUnit.AURA_APPLICATIONS:         FieldsType.FOUR_BYTES,
    FieldUnit.AURA_FLAGS:                FieldsType.FOUR_BYTES,
    FieldUnit.AURA_STATE:                FieldsType.INT32,

    FieldUnit.BASE_ATTACK_TIME:          FieldsType.INT32,
    FieldUnit.OFFHAND_ATTACK_TIME:       FieldsType.INT32,
    FieldUnit.RANGED_ATTACK_TIME:        FieldsType.INT32,

    FieldUnit.BOUNDING_RADIUS:           FieldsType.FLOAT,
    FieldUnit.COMBAT_REACH:              FieldsType.FLOAT,

    FieldUnit.DISPLAY_ID:                FieldsType.INT32,
    FieldUnit.NATIVE_DISPLAY_ID:         FieldsType.INT32,
    FieldUnit.MOUNT_DISPLAY_ID:          FieldsType.INT32,

    FieldUnit.MIN_DAMAGE:                FieldsType.FLOAT,
    FieldUnit.MAX_DAMAGE:                FieldsType.FLOAT,
    FieldUnit.MIN_OFFHAND_DAMAGE:        FieldsType.FLOAT,
    FieldUnit.MAX_OFFHAND_DAMAGE:        FieldsType.FLOAT,

    FieldUnit.BYTES_1:                   FieldsType.FOUR_BYTES,

    FieldUnit.PET_NUMBER:                FieldsType.INT32,
    FieldUnit.PET_NAME_TIMESTAMP:        FieldsType.INT32,
    FieldUnit.PET_EXPERIENCE:            FieldsType.INT32,
    FieldUnit.PET_NEXT_LEVEL_EXP:        FieldsType.INT32,

    FieldUnit.DYNAMIC_FLAGS:             FieldsType.INT32,
    FieldUnit.CHANNEL_SPELL:             FieldsType.INT32,
    FieldUnit.MOD_CAST_SPEED:            FieldsType.INT32,
    FieldUnit.CREATED_BY_SPELL:          FieldsType.INT32,

    FieldUnit.NPC_FLAGS:                 FieldsType.INT32,
    FieldUnit.NPC_EMOTESTATE:            FieldsType.INT32,

    FieldUnit.TRAINING_POINTS:           FieldsType.TWO_INT16,

    FieldUnit.STAT_0:                    FieldsType.INT32,
    FieldUnit.STAT_1:                    FieldsType.INT32,
    FieldUnit.STAT_2:                    FieldsType.INT32,
    FieldUnit.STAT_3:                    FieldsType.INT32,
    FieldUnit.STAT_4:                    FieldsType.INT32,
    FieldUnit.RESISTANCE_0:              FieldsType.INT32,
    FieldUnit.RESISTANCE_1:              FieldsType.INT32,
    FieldUnit.RESISTANCE_2:              FieldsType.INT32,
    FieldUnit.RESISTANCE_3:              FieldsType.INT32,
    FieldUnit.RESISTANCE_4:              FieldsType.INT32,
    FieldUnit.RESISTANCE_5:              FieldsType.INT32,
    FieldUnit.RESISTANCE_6:              FieldsType.INT32,

    FieldUnit.ATTACK_POWER:              FieldsType.INT32,
    FieldUnit.BASE_MANA:                 FieldsType.INT32,
    FieldUnit.ATTACK_POWER_MODS:         FieldsType.TWO_INT16,

    FieldUnit.BYTES_2:                   FieldsType.FOUR_BYTES,

    FieldUnit.RANGED_ATTACK_POWER:       FieldsType.INT32,
    FieldUnit.RANGED_ATTACK_POWER_MODS:  FieldsType.TWO_INT16,
    FieldUnit.MIN_RANGED_DAMAGE:         FieldsType.FLOAT,
    FieldUnit.MAX_RANGED_DAMAGE:         FieldsType.FLOAT,

    # --------------------
    # Player fields
    # --------------------

    FieldPlayer.SELECTION:                 FieldsType.INT64,
    FieldPlayer.DUEL_ARBITER:              FieldsType.INT64,
    FieldPlayer.FLAGS:                     FieldsType.INT32,

    FieldPlayer.GUILD_ID:                  FieldsType.INT32,
    FieldPlayer.GUILD_RANK:                FieldsType.INT32,

    FieldPlayer.BYTES_1:                   FieldsType.FOUR_BYTES,
    FieldPlayer.BYTES_2:                   FieldsType.FOUR_BYTES,
    FieldPlayer.BYTES_3:                   FieldsType.FOUR_BYTES,

    FieldPlayer.DUEL_TEAM:                 FieldsType.INT32,
    FieldPlayer.GUILD_TIMESTAMP:           FieldsType.INT32,

    FieldPlayer.INV_SLOT_HEAD:             FieldsType.INT64,

    FieldPlayer.PACK_SLOT_1:               FieldsType.INT64,

    FieldPlayer.BANK_SLOT_1:               FieldsType.INT64,

    FieldPlayer.BANK_BAG_SLOT_1:           FieldsType.INT64,

    FieldPlayer.VENDOR_BUY_BACK_SLOT:      FieldsType.INT64,

    FieldPlayer.FAR_SIGHT:                 FieldsType.INT64,
    FieldPlayer.COMBO_TARGET:              FieldsType.INT64,

    FieldPlayer.BUY_BACK_NPC:              FieldsType.INT64,

    FieldPlayer.EXP:                       FieldsType.INT32,
    FieldPlayer.NEXT_LEVEL_EXP:            FieldsType.INT32,

    FieldPlayer.SKILL_INFO_1_1:            FieldsType.TWO_INT16,

    FieldPlayer.QUEST_LOG_1_1:             FieldsType.INT32,

    FieldPlayer.CHARACTER_POINTS_1:        FieldsType.INT32,
    FieldPlayer.CHARACTER_POINTS_2:        FieldsType.INT32,

    FieldPlayer.TRACK_CREATURES:           FieldsType.INT32,
    FieldPlayer.TRACK_RESOURCES:           FieldsType.INT32,

    FieldPlayer.CHAT_FILTERS:              FieldsType.INT32,

    FieldPlayer.BLOCK_PERCENTAGE:          FieldsType.FLOAT,
    FieldPlayer.DODGE_PERCENTAGE:          FieldsType.FLOAT,
    FieldPlayer.PARRY_PERCENTAGE:          FieldsType.FLOAT,
    FieldPlayer.CRIT_PERCENTAGE:           FieldsType.FLOAT,

    FieldPlayer.EXPLORED_ZONES_1:          FieldsType.FOUR_BYTES,
    FieldPlayer.EXPLORED_ZONES_2:          FieldsType.FOUR_BYTES,
    FieldPlayer.EXPLORED_ZONES_3:          FieldsType.FOUR_BYTES,
    FieldPlayer.EXPLORED_ZONES_4:          FieldsType.FOUR_BYTES,
    FieldPlayer.EXPLORED_ZONES_5:          FieldsType.FOUR_BYTES,
    FieldPlayer.EXPLORED_ZONES_6:          FieldsType.FOUR_BYTES,
    FieldPlayer.EXPLORED_ZONES_7:          FieldsType.FOUR_BYTES,
    FieldPlayer.EXPLORED_ZONES_8:          FieldsType.FOUR_BYTES,
    FieldPlayer.EXPLORED_ZONES_9:          FieldsType.FOUR_BYTES,
    FieldPlayer.EXPLORED_ZONES_10:         FieldsType.FOUR_BYTES,
    FieldPlayer.EXPLORED_ZONES_11:         FieldsType.FOUR_BYTES,
    FieldPlayer.EXPLORED_ZONES_12:         FieldsType.FOUR_BYTES,
    FieldPlayer.EXPLORED_ZONES_13:         FieldsType.FOUR_BYTES,
    FieldPlayer.EXPLORED_ZONES_14:         FieldsType.FOUR_BYTES,
    FieldPlayer.EXPLORED_ZONES_15:         FieldsType.FOUR_BYTES,
    FieldPlayer.EXPLORED_ZONES_16:         FieldsType.FOUR_BYTES,
    FieldPlayer.EXPLORED_ZONES_17:         FieldsType.FOUR_BYTES,
    FieldPlayer.EXPLORED_ZONES_18:         FieldsType.FOUR_BYTES,
    FieldPlayer.EXPLORED_ZONES_19:         FieldsType.FOUR_BYTES,
    FieldPlayer.EXPLORED_ZONES_20:         FieldsType.FOUR_BYTES,
    FieldPlayer.EXPLORED_ZONES_21:         FieldsType.FOUR_BYTES,
    FieldPlayer.EXPLORED_ZONES_22:         FieldsType.FOUR_BYTES,
    FieldPlayer.EXPLORED_ZONES_23:         FieldsType.FOUR_BYTES,
    FieldPlayer.EXPLORED_ZONES_24:         FieldsType.FOUR_BYTES,
    FieldPlayer.EXPLORED_ZONES_25:         FieldsType.FOUR_BYTES,
    FieldPlayer.EXPLORED_ZONES_26:         FieldsType.FOUR_BYTES,
    FieldPlayer.EXPLORED_ZONES_27:         FieldsType.FOUR_BYTES,
    FieldPlayer.EXPLORED_ZONES_28:         FieldsType.FOUR_BYTES,
    FieldPlayer.EXPLORED_ZONES_29:         FieldsType.FOUR_BYTES,
    FieldPlayer.EXPLORED_ZONES_30:         FieldsType.FOUR_BYTES,
    FieldPlayer.EXPLORED_ZONES_31:         FieldsType.FOUR_BYTES,
    FieldPlayer.EXPLORED_ZONES_32:         FieldsType.FOUR_BYTES,

    FieldPlayer.REST_STATE_EXP:            FieldsType.INT32,
    FieldPlayer.COINAGE:                   FieldsType.INT32,

    FieldPlayer.POS_STAT_0:                FieldsType.INT32,
    FieldPlayer.POS_STAT_1:                FieldsType.INT32,
    FieldPlayer.POS_STAT_2:                FieldsType.INT32,
    FieldPlayer.POS_STAT_3:                FieldsType.INT32,
    FieldPlayer.POS_STAT_4:                FieldsType.INT32,
    FieldPlayer.NEG_STAT_0:                FieldsType.INT32,
    FieldPlayer.NEG_STAT_1:                FieldsType.INT32,
    FieldPlayer.NEG_STAT_2:                FieldsType.INT32,
    FieldPlayer.NEG_STAT_3:                FieldsType.INT32,
    FieldPlayer.NEG_STAT_4:                FieldsType.INT32,

    FieldPlayer.RESISTANCE_0_BUFF_MOD_POS: FieldsType.INT32,
    FieldPlayer.RESISTANCE_1_BUFF_MOD_POS: FieldsType.INT32,
    FieldPlayer.RESISTANCE_2_BUFF_MOD_POS: FieldsType.INT32,
    FieldPlayer.RESISTANCE_3_BUFF_MOD_POS: FieldsType.INT32,
    FieldPlayer.RESISTANCE_4_BUFF_MOD_POS: FieldsType.INT32,
    FieldPlayer.RESISTANCE_5_BUFF_MOD_POS: FieldsType.INT32,
    FieldPlayer.RESISTANCE_6_BUFF_MOD_POS: FieldsType.INT32,
    FieldPlayer.RESISTANCE_0_BUFF_MOD_NEG: FieldsType.INT32,
    FieldPlayer.RESISTANCE_1_BUFF_MOD_NEG: FieldsType.INT32,
    FieldPlayer.RESISTANCE_2_BUFF_MOD_NEG: FieldsType.INT32,
    FieldPlayer.RESISTANCE_3_BUFF_MOD_NEG: FieldsType.INT32,
    FieldPlayer.RESISTANCE_4_BUFF_MOD_NEG: FieldsType.INT32,
    FieldPlayer.RESISTANCE_5_BUFF_MOD_NEG: FieldsType.INT32,
    FieldPlayer.RESISTANCE_6_BUFF_MOD_NEG: FieldsType.INT32,

    FieldPlayer.MOD_DAMAGE_0_DONE_POS:     FieldsType.INT32,
    FieldPlayer.MOD_DAMAGE_1_DONE_POS:     FieldsType.INT32,
    FieldPlayer.MOD_DAMAGE_2_DONE_POS:     FieldsType.INT32,
    FieldPlayer.MOD_DAMAGE_3_DONE_POS:     FieldsType.INT32,
    FieldPlayer.MOD_DAMAGE_4_DONE_POS:     FieldsType.INT32,
    FieldPlayer.MOD_DAMAGE_5_DONE_POS:     FieldsType.INT32,
    FieldPlayer.MOD_DAMAGE_6_DONE_POS:     FieldsType.INT32,
    FieldPlayer.MOD_DAMAGE_0_DONE_NEG:     FieldsType.INT32,
    FieldPlayer.MOD_DAMAGE_1_DONE_NEG:     FieldsType.INT32,
    FieldPlayer.MOD_DAMAGE_2_DONE_NEG:     FieldsType.INT32,
    FieldPlayer.MOD_DAMAGE_3_DONE_NEG:     FieldsType.INT32,
    FieldPlayer.MOD_DAMAGE_4_DONE_NEG:     FieldsType.INT32,
    FieldPlayer.MOD_DAMAGE_5_DONE_NEG:     FieldsType.INT32,
    FieldPlayer.MOD_DAMAGE_6_DONE_NEG:     FieldsType.INT32,
    FieldPlayer.MOD_DAMAGE_0_DONE_PCT:     FieldsType.INT32,
    FieldPlayer.MOD_DAMAGE_1_DONE_PCT:     FieldsType.INT32,
    FieldPlayer.MOD_DAMAGE_2_DONE_PCT:     FieldsType.INT32,
    FieldPlayer.MOD_DAMAGE_3_DONE_PCT:     FieldsType.INT32,
    FieldPlayer.MOD_DAMAGE_4_DONE_PCT:     FieldsType.INT32,
    FieldPlayer.MOD_DAMAGE_5_DONE_PCT:     FieldsType.INT32,
    FieldPlayer.MOD_DAMAGE_6_DONE_PCT:     FieldsType.INT32,

    FieldPlayer.BYTES_4:                   FieldsType.FOUR_BYTES,

    FieldPlayer.AMMO_ID:                   FieldsType.INT32,

    FieldPlayer.PVP_MEDALS:                FieldsType.INT32,

    FieldPlayer.BUYBACK_ITEM_ID:           FieldsType.INT32,
    FieldPlayer.BUYBACK_RANDOM_PROP_ID:    FieldsType.INT32,
    FieldPlayer.BUYBACK_SEED:              FieldsType.INT32,
    FieldPlayer.BUYBACK_PRICE:             FieldsType.INT32,

    # --------------------
    # Game object fields
    # --------------------

    FieldGameObject.DISPLAY_ID: FieldsType.INT32,
    FieldGameObject.FLAGS:      FieldsType.INT32,

    FieldGameObject.ROTATION_1: FieldsType.FLOAT,
    FieldGameObject.ROTATION_2: FieldsType.FLOAT,
    FieldGameObject.ROTATION_3: FieldsType.FLOAT,
    FieldGameObject.ROTATION_4: FieldsType.FLOAT,

    FieldGameObject.STATE:      FieldsType.INT32,
    FieldGameObject.TIMESTAMP:  FieldsType.INT32,

    FieldGameObject.POS_X:      FieldsType.FLOAT,
    FieldGameObject.POS_Y:      FieldsType.FLOAT,
    FieldGameObject.POS_Z:      FieldsType.FLOAT,
    FieldGameObject.FACING:     FieldsType.FLOAT,

    FieldGameObject.DYN_FLAGS:  FieldsType.INT32,
    FieldGameObject.FACTION:    FieldsType.INT32,
    FieldGameObject.TYPE_ID:    FieldsType.INT32,
    FieldGameObject.LEVEL:      FieldsType.INT32,

    # --------------------
    # Dynamic object fields
    # --------------------

    FieldDynamicObject.CASTER:   FieldsType.INT64,
    FieldDynamicObject.BYTES:    FieldsType.FOUR_BYTES,
    FieldDynamicObject.SPELL_ID: FieldsType.INT32,
    FieldDynamicObject.RADIUS:   FieldsType.FLOAT,

    FieldDynamicObject.POS_X:    FieldsType.FLOAT,
    FieldDynamicObject.POS_Y:    FieldsType.FLOAT,
    FieldDynamicObject.POS_Z:    FieldsType.FLOAT,
    FieldDynamicObject.FACING:   FieldsType.FLOAT,

    # --------------------
    # Corpse fields
    # --------------------

    FieldCorpse.OWNER:      FieldsType.INT64,

    FieldCorpse.FACING:     FieldsType.FLOAT,
    FieldCorpse.POS_X:      FieldsType.FLOAT,
    FieldCorpse.POS_Y:      FieldsType.FLOAT,
    FieldCorpse.POS_Z:      FieldsType.FLOAT,

    FieldCorpse.DISPLAY_ID: FieldsType.INT32,

    FieldCorpse.ITEM_1:     FieldsType.INT32,
    FieldCorpse.ITEM_2:     FieldsType.INT32,
    FieldCorpse.ITEM_3:     FieldsType.INT32,
    FieldCorpse.ITEM_4:     FieldsType.INT32,
    FieldCorpse.ITEM_5:     FieldsType.INT32,
    FieldCorpse.ITEM_6:     FieldsType.INT32,
    FieldCorpse.ITEM_7:     FieldsType.INT32,
    FieldCorpse.ITEM_8:     FieldsType.INT32,
    FieldCorpse.ITEM_9:     FieldsType.INT32,
    FieldCorpse.ITEM_10:    FieldsType.INT32,
    FieldCorpse.ITEM_11:    FieldsType.INT32,
    FieldCorpse.ITEM_12:    FieldsType.INT32,
    FieldCorpse.ITEM_13:    FieldsType.INT32,
    FieldCorpse.ITEM_14:    FieldsType.INT32,
    FieldCorpse.ITEM_15:    FieldsType.INT32,
    FieldCorpse.ITEM_16:    FieldsType.INT32,
    FieldCorpse.ITEM_17:    FieldsType.INT32,
    FieldCorpse.ITEM_18:    FieldsType.INT32,
    FieldCorpse.ITEM_19:    FieldsType.INT32,

    FieldCorpse.BYTES_1:    FieldsType.FOUR_BYTES,
    FieldCorpse.BYTES_2:    FieldsType.FOUR_BYTES,

    FieldCorpse.GUILD:      FieldsType.INT32,
    FieldCorpse.FLAGS:      FieldsType.INT32
}
