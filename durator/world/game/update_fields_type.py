""" Map all used update fields to an update type. """

from enum import Enum

from durator.world.game.update_fields import (
    UpdateFieldObject, UpdateFieldItem, UpdateFieldContainer,
    UpdateFieldUnit, UpdateFieldPlayer,
    UpdateFieldDynamicObject, UpdateFieldGameObject, UpdateFieldCorpse )


class UpdateFieldsType(Enum):

    INT32      = 1
    TWO_INT16  = 2
    FLOAT      = 3
    INT64      = 4
    FOUR_BYTES = 5


UPDATE_FIELD_TYPE_MAP = {

    # --------------------
    # Object fields
    # --------------------

    UpdateFieldObject.GUID:    UpdateFieldsType.INT64,
    UpdateFieldObject.TYPE:    UpdateFieldsType.INT32,
    UpdateFieldObject.ENTRY:   UpdateFieldsType.INT32,
    UpdateFieldObject.SCALE_X: UpdateFieldsType.FLOAT,

    # --------------------
    # Item fields
    # --------------------

    UpdateFieldItem.OWNER:                UpdateFieldsType.INT64,
    UpdateFieldItem.CONTAINED:            UpdateFieldsType.INT64,
    UpdateFieldItem.CREATOR:              UpdateFieldsType.INT64,
    UpdateFieldItem.GIFTCREATOR:          UpdateFieldsType.INT64,

    UpdateFieldItem.STACK_COUNT:          UpdateFieldsType.INT32,
    UpdateFieldItem.DURATION:             UpdateFieldsType.INT32,
    UpdateFieldItem.SPELL_CHARGES:        UpdateFieldsType.INT32,

    UpdateFieldItem.FLAGS:                UpdateFieldsType.TWO_INT16,

    UpdateFieldItem.ENCHANTMENT:          UpdateFieldsType.INT32,

    UpdateFieldItem.PROPERTY_SEED:        UpdateFieldsType.INT32,
    UpdateFieldItem.RANDOM_PROPERTIES_ID: UpdateFieldsType.INT32,
    UpdateFieldItem.ITEM_TEXT_ID:         UpdateFieldsType.INT32,

    UpdateFieldItem.DURABILITY:           UpdateFieldsType.INT32,
    UpdateFieldItem.MAX_DURABILITY:       UpdateFieldsType.INT32,

    # --------------------
    # Container fields
    # --------------------

    UpdateFieldContainer.NUM_SLOTS: UpdateFieldsType.INT32,
    UpdateFieldContainer.SLOT_1:    UpdateFieldsType.INT64,

    # --------------------
    # Unit fields
    # --------------------

    UpdateFieldUnit.CHARM:                     UpdateFieldsType.INT64,
    UpdateFieldUnit.SUMMON:                    UpdateFieldsType.INT64,
    UpdateFieldUnit.CHARMED_BY:                UpdateFieldsType.INT64,
    UpdateFieldUnit.SUMMONED_BY:               UpdateFieldsType.INT64,
    UpdateFieldUnit.CREATED_BY:                UpdateFieldsType.INT64,
    UpdateFieldUnit.TARGET:                    UpdateFieldsType.INT64,
    UpdateFieldUnit.PERSUADED:                 UpdateFieldsType.INT64,
    UpdateFieldUnit.CHANNEL_OBJECT:            UpdateFieldsType.INT64,

    UpdateFieldUnit.HEALTH:                    UpdateFieldsType.INT32,
    UpdateFieldUnit.POWER_1:                   UpdateFieldsType.INT32,
    UpdateFieldUnit.POWER_2:                   UpdateFieldsType.INT32,
    UpdateFieldUnit.POWER_3:                   UpdateFieldsType.INT32,
    UpdateFieldUnit.POWER_4:                   UpdateFieldsType.INT32,
    UpdateFieldUnit.POWER_5:                   UpdateFieldsType.INT32,

    UpdateFieldUnit.MAX_HEALTH:                UpdateFieldsType.INT32,
    UpdateFieldUnit.MAX_POWER_1:               UpdateFieldsType.INT32,
    UpdateFieldUnit.MAX_POWER_2:               UpdateFieldsType.INT32,
    UpdateFieldUnit.MAX_POWER_3:               UpdateFieldsType.INT32,
    UpdateFieldUnit.MAX_POWER_4:               UpdateFieldsType.INT32,
    UpdateFieldUnit.MAX_POWER_5:               UpdateFieldsType.INT32,

    UpdateFieldUnit.LEVEL:                     UpdateFieldsType.INT32,
    UpdateFieldUnit.FACTION_TEMPLATE:          UpdateFieldsType.INT32,
    UpdateFieldUnit.BYTES_0:                   UpdateFieldsType.FOUR_BYTES,
    UpdateFieldUnit.VIRTUAL_ITEM_SLOT_DISPLAY: UpdateFieldsType.INT32,
    UpdateFieldUnit.VIRTUAL_ITEM_INFO:         UpdateFieldsType.FOUR_BYTES,
    UpdateFieldUnit.FLAGS:                     UpdateFieldsType.INT32,

    UpdateFieldUnit.AURA:                      UpdateFieldsType.INT32,
    UpdateFieldUnit.AURA_LEVELS:               UpdateFieldsType.FOUR_BYTES,
    UpdateFieldUnit.AURA_APPLICATIONS:         UpdateFieldsType.FOUR_BYTES,
    UpdateFieldUnit.AURA_FLAGS:                UpdateFieldsType.FOUR_BYTES,
    UpdateFieldUnit.AURA_STATE:                UpdateFieldsType.INT32,

    UpdateFieldUnit.BASE_ATTACK_TIME:          UpdateFieldsType.INT32,
    UpdateFieldUnit.OFFHAND_ATTACK_TIME:       UpdateFieldsType.INT32,
    UpdateFieldUnit.RANGED_ATTACK_TIME:        UpdateFieldsType.INT32,

    UpdateFieldUnit.BOUNDING_RADIUS:           UpdateFieldsType.FLOAT,
    UpdateFieldUnit.COMBAT_REACH:              UpdateFieldsType.FLOAT,

    UpdateFieldUnit.DISPLAY_ID:                UpdateFieldsType.INT32,
    UpdateFieldUnit.NATIVE_DISPLAY_ID:         UpdateFieldsType.INT32,
    UpdateFieldUnit.MOUNT_DISPLAY_ID:          UpdateFieldsType.INT32,

    UpdateFieldUnit.MIN_DAMAGE:                UpdateFieldsType.FLOAT,
    UpdateFieldUnit.MAX_DAMAGE:                UpdateFieldsType.FLOAT,
    UpdateFieldUnit.MIN_OFFHAND_DAMAGE:        UpdateFieldsType.FLOAT,
    UpdateFieldUnit.MAX_OFFHAND_DAMAGE:        UpdateFieldsType.FLOAT,

    UpdateFieldUnit.BYTES_1:                   UpdateFieldsType.FOUR_BYTES,

    UpdateFieldUnit.PET_NUMBER:                UpdateFieldsType.INT32,
    UpdateFieldUnit.PET_NAME_TIMESTAMP:        UpdateFieldsType.INT32,
    UpdateFieldUnit.PET_EXPERIENCE:            UpdateFieldsType.INT32,
    UpdateFieldUnit.PET_NEXT_LEVEL_EXP:        UpdateFieldsType.INT32,

    UpdateFieldUnit.DYNAMIC_FLAGS:             UpdateFieldsType.INT32,
    UpdateFieldUnit.CHANNEL_SPELL:             UpdateFieldsType.INT32,
    UpdateFieldUnit.MOD_CAST_SPEED:            UpdateFieldsType.INT32,
    UpdateFieldUnit.CREATED_BY_SPELL:          UpdateFieldsType.INT32,

    UpdateFieldUnit.NPC_FLAGS:                 UpdateFieldsType.INT32,
    UpdateFieldUnit.NPC_EMOTESTATE:            UpdateFieldsType.INT32,

    UpdateFieldUnit.TRAINING_POINTS:           UpdateFieldsType.TWO_INT16,

    UpdateFieldUnit.STAT_0:                    UpdateFieldsType.INT32,
    UpdateFieldUnit.STAT_1:                    UpdateFieldsType.INT32,
    UpdateFieldUnit.STAT_2:                    UpdateFieldsType.INT32,
    UpdateFieldUnit.STAT_3:                    UpdateFieldsType.INT32,
    UpdateFieldUnit.STAT_4:                    UpdateFieldsType.INT32,
    UpdateFieldUnit.RESISTANCE_0:              UpdateFieldsType.INT32,
    UpdateFieldUnit.RESISTANCE_1:              UpdateFieldsType.INT32,
    UpdateFieldUnit.RESISTANCE_2:              UpdateFieldsType.INT32,
    UpdateFieldUnit.RESISTANCE_3:              UpdateFieldsType.INT32,
    UpdateFieldUnit.RESISTANCE_4:              UpdateFieldsType.INT32,
    UpdateFieldUnit.RESISTANCE_5:              UpdateFieldsType.INT32,
    UpdateFieldUnit.RESISTANCE_6:              UpdateFieldsType.INT32,

    UpdateFieldUnit.ATTACK_POWER:              UpdateFieldsType.INT32,
    UpdateFieldUnit.BASE_MANA:                 UpdateFieldsType.INT32,
    UpdateFieldUnit.ATTACK_POWER_MODS:         UpdateFieldsType.TWO_INT16,

    UpdateFieldUnit.BYTES_2:                   UpdateFieldsType.FOUR_BYTES,

    UpdateFieldUnit.RANGED_ATTACK_POWER:       UpdateFieldsType.INT32,
    UpdateFieldUnit.RANGED_ATTACK_POWER_MODS:  UpdateFieldsType.TWO_INT16,
    UpdateFieldUnit.MIN_RANGED_DAMAGE:         UpdateFieldsType.FLOAT,
    UpdateFieldUnit.MAX_RANGED_DAMAGE:         UpdateFieldsType.FLOAT,

    # --------------------
    # Player fields
    # --------------------

    UpdateFieldPlayer.SELECTION:                 UpdateFieldsType.INT64,
    UpdateFieldPlayer.DUEL_ARBITER:              UpdateFieldsType.INT64,
    UpdateFieldPlayer.FLAGS:                     UpdateFieldsType.INT32,

    UpdateFieldPlayer.GUILD_ID:                  UpdateFieldsType.INT32,
    UpdateFieldPlayer.GUILD_RANK:                UpdateFieldsType.INT32,

    UpdateFieldPlayer.BYTES_1:                   UpdateFieldsType.FOUR_BYTES,
    UpdateFieldPlayer.BYTES_2:                   UpdateFieldsType.FOUR_BYTES,
    UpdateFieldPlayer.BYTES_3:                   UpdateFieldsType.FOUR_BYTES,

    UpdateFieldPlayer.DUEL_TEAM:                 UpdateFieldsType.INT32,
    UpdateFieldPlayer.GUILD_TIMESTAMP:           UpdateFieldsType.INT32,

    UpdateFieldPlayer.INV_SLOT_HEAD:             UpdateFieldsType.INT64,

    UpdateFieldPlayer.PACK_SLOT_1:               UpdateFieldsType.INT64,

    UpdateFieldPlayer.BANK_SLOT_1:               UpdateFieldsType.INT64,

    UpdateFieldPlayer.BANK_BAG_SLOT_1:           UpdateFieldsType.INT64,

    UpdateFieldPlayer.VENDOR_BUY_BACK_SLOT:      UpdateFieldsType.INT64,

    UpdateFieldPlayer.FAR_SIGHT:                 UpdateFieldsType.INT64,
    UpdateFieldPlayer.COMBO_TARGET:              UpdateFieldsType.INT64,

    UpdateFieldPlayer.BUY_BACK_NPC:              UpdateFieldsType.INT64,

    UpdateFieldPlayer.EXP:                       UpdateFieldsType.INT32,
    UpdateFieldPlayer.NEXT_LEVEL_XP:             UpdateFieldsType.INT32,

    UpdateFieldPlayer.SKILL_INFO_1_1:            UpdateFieldsType.TWO_INT16,

    UpdateFieldPlayer.QUEST_LOG_1_1:             UpdateFieldsType.INT32,

    UpdateFieldPlayer.CHARACTER_POINTS_1:        UpdateFieldsType.INT32,
    UpdateFieldPlayer.CHARACTER_POINTS_2:        UpdateFieldsType.INT32,

    UpdateFieldPlayer.TRACK_CREATURES:           UpdateFieldsType.INT32,
    UpdateFieldPlayer.TRACK_RESOURCES:           UpdateFieldsType.INT32,

    UpdateFieldPlayer.CHAT_FILTERS:              UpdateFieldsType.INT32,

    UpdateFieldPlayer.BLOCK_PERCENTAGE:          UpdateFieldsType.FLOAT,
    UpdateFieldPlayer.DODGE_PERCENTAGE:          UpdateFieldsType.FLOAT,
    UpdateFieldPlayer.PARRY_PERCENTAGE:          UpdateFieldsType.FLOAT,
    UpdateFieldPlayer.CRIT_PERCENTAGE:           UpdateFieldsType.FLOAT,

    UpdateFieldPlayer.EXPLORED_ZONES_1:          UpdateFieldsType.FOUR_BYTES,
    UpdateFieldPlayer.EXPLORED_ZONES_2:          UpdateFieldsType.FOUR_BYTES,
    UpdateFieldPlayer.EXPLORED_ZONES_3:          UpdateFieldsType.FOUR_BYTES,
    UpdateFieldPlayer.EXPLORED_ZONES_4:          UpdateFieldsType.FOUR_BYTES,
    UpdateFieldPlayer.EXPLORED_ZONES_5:          UpdateFieldsType.FOUR_BYTES,
    UpdateFieldPlayer.EXPLORED_ZONES_6:          UpdateFieldsType.FOUR_BYTES,
    UpdateFieldPlayer.EXPLORED_ZONES_7:          UpdateFieldsType.FOUR_BYTES,
    UpdateFieldPlayer.EXPLORED_ZONES_8:          UpdateFieldsType.FOUR_BYTES,
    UpdateFieldPlayer.EXPLORED_ZONES_9:          UpdateFieldsType.FOUR_BYTES,
    UpdateFieldPlayer.EXPLORED_ZONES_10:         UpdateFieldsType.FOUR_BYTES,
    UpdateFieldPlayer.EXPLORED_ZONES_11:         UpdateFieldsType.FOUR_BYTES,
    UpdateFieldPlayer.EXPLORED_ZONES_12:         UpdateFieldsType.FOUR_BYTES,
    UpdateFieldPlayer.EXPLORED_ZONES_13:         UpdateFieldsType.FOUR_BYTES,
    UpdateFieldPlayer.EXPLORED_ZONES_14:         UpdateFieldsType.FOUR_BYTES,
    UpdateFieldPlayer.EXPLORED_ZONES_15:         UpdateFieldsType.FOUR_BYTES,
    UpdateFieldPlayer.EXPLORED_ZONES_16:         UpdateFieldsType.FOUR_BYTES,
    UpdateFieldPlayer.EXPLORED_ZONES_17:         UpdateFieldsType.FOUR_BYTES,
    UpdateFieldPlayer.EXPLORED_ZONES_18:         UpdateFieldsType.FOUR_BYTES,
    UpdateFieldPlayer.EXPLORED_ZONES_19:         UpdateFieldsType.FOUR_BYTES,
    UpdateFieldPlayer.EXPLORED_ZONES_20:         UpdateFieldsType.FOUR_BYTES,
    UpdateFieldPlayer.EXPLORED_ZONES_21:         UpdateFieldsType.FOUR_BYTES,
    UpdateFieldPlayer.EXPLORED_ZONES_22:         UpdateFieldsType.FOUR_BYTES,
    UpdateFieldPlayer.EXPLORED_ZONES_23:         UpdateFieldsType.FOUR_BYTES,
    UpdateFieldPlayer.EXPLORED_ZONES_24:         UpdateFieldsType.FOUR_BYTES,
    UpdateFieldPlayer.EXPLORED_ZONES_25:         UpdateFieldsType.FOUR_BYTES,
    UpdateFieldPlayer.EXPLORED_ZONES_26:         UpdateFieldsType.FOUR_BYTES,
    UpdateFieldPlayer.EXPLORED_ZONES_27:         UpdateFieldsType.FOUR_BYTES,
    UpdateFieldPlayer.EXPLORED_ZONES_28:         UpdateFieldsType.FOUR_BYTES,
    UpdateFieldPlayer.EXPLORED_ZONES_29:         UpdateFieldsType.FOUR_BYTES,
    UpdateFieldPlayer.EXPLORED_ZONES_30:         UpdateFieldsType.FOUR_BYTES,
    UpdateFieldPlayer.EXPLORED_ZONES_31:         UpdateFieldsType.FOUR_BYTES,
    UpdateFieldPlayer.EXPLORED_ZONES_32:         UpdateFieldsType.FOUR_BYTES,

    UpdateFieldPlayer.REST_STATE_EXPERIENCE:     UpdateFieldsType.INT32,
    UpdateFieldPlayer.COINAGE:                   UpdateFieldsType.INT32,

    UpdateFieldPlayer.POS_STAT_0:                UpdateFieldsType.INT32,
    UpdateFieldPlayer.POS_STAT_1:                UpdateFieldsType.INT32,
    UpdateFieldPlayer.POS_STAT_2:                UpdateFieldsType.INT32,
    UpdateFieldPlayer.POS_STAT_3:                UpdateFieldsType.INT32,
    UpdateFieldPlayer.POS_STAT_4:                UpdateFieldsType.INT32,
    UpdateFieldPlayer.NEG_STAT_0:                UpdateFieldsType.INT32,
    UpdateFieldPlayer.NEG_STAT_1:                UpdateFieldsType.INT32,
    UpdateFieldPlayer.NEG_STAT_2:                UpdateFieldsType.INT32,
    UpdateFieldPlayer.NEG_STAT_3:                UpdateFieldsType.INT32,
    UpdateFieldPlayer.NEG_STAT_4:                UpdateFieldsType.INT32,

    UpdateFieldPlayer.RESISTANCE_0_BUFF_MOD_POS: UpdateFieldsType.INT32,
    UpdateFieldPlayer.RESISTANCE_1_BUFF_MOD_POS: UpdateFieldsType.INT32,
    UpdateFieldPlayer.RESISTANCE_2_BUFF_MOD_POS: UpdateFieldsType.INT32,
    UpdateFieldPlayer.RESISTANCE_3_BUFF_MOD_POS: UpdateFieldsType.INT32,
    UpdateFieldPlayer.RESISTANCE_4_BUFF_MOD_POS: UpdateFieldsType.INT32,
    UpdateFieldPlayer.RESISTANCE_5_BUFF_MOD_POS: UpdateFieldsType.INT32,
    UpdateFieldPlayer.RESISTANCE_6_BUFF_MOD_POS: UpdateFieldsType.INT32,
    UpdateFieldPlayer.RESISTANCE_0_BUFF_MOD_NEG: UpdateFieldsType.INT32,
    UpdateFieldPlayer.RESISTANCE_1_BUFF_MOD_NEG: UpdateFieldsType.INT32,
    UpdateFieldPlayer.RESISTANCE_2_BUFF_MOD_NEG: UpdateFieldsType.INT32,
    UpdateFieldPlayer.RESISTANCE_3_BUFF_MOD_NEG: UpdateFieldsType.INT32,
    UpdateFieldPlayer.RESISTANCE_4_BUFF_MOD_NEG: UpdateFieldsType.INT32,
    UpdateFieldPlayer.RESISTANCE_5_BUFF_MOD_NEG: UpdateFieldsType.INT32,
    UpdateFieldPlayer.RESISTANCE_6_BUFF_MOD_NEG: UpdateFieldsType.INT32,

    UpdateFieldPlayer.MOD_DAMAGE_0_DONE_POS:     UpdateFieldsType.INT32,
    UpdateFieldPlayer.MOD_DAMAGE_1_DONE_POS:     UpdateFieldsType.INT32,
    UpdateFieldPlayer.MOD_DAMAGE_2_DONE_POS:     UpdateFieldsType.INT32,
    UpdateFieldPlayer.MOD_DAMAGE_3_DONE_POS:     UpdateFieldsType.INT32,
    UpdateFieldPlayer.MOD_DAMAGE_4_DONE_POS:     UpdateFieldsType.INT32,
    UpdateFieldPlayer.MOD_DAMAGE_5_DONE_POS:     UpdateFieldsType.INT32,
    UpdateFieldPlayer.MOD_DAMAGE_6_DONE_POS:     UpdateFieldsType.INT32,
    UpdateFieldPlayer.MOD_DAMAGE_0_DONE_NEG:     UpdateFieldsType.INT32,
    UpdateFieldPlayer.MOD_DAMAGE_1_DONE_NEG:     UpdateFieldsType.INT32,
    UpdateFieldPlayer.MOD_DAMAGE_2_DONE_NEG:     UpdateFieldsType.INT32,
    UpdateFieldPlayer.MOD_DAMAGE_3_DONE_NEG:     UpdateFieldsType.INT32,
    UpdateFieldPlayer.MOD_DAMAGE_4_DONE_NEG:     UpdateFieldsType.INT32,
    UpdateFieldPlayer.MOD_DAMAGE_5_DONE_NEG:     UpdateFieldsType.INT32,
    UpdateFieldPlayer.MOD_DAMAGE_6_DONE_NEG:     UpdateFieldsType.INT32,
    UpdateFieldPlayer.MOD_DAMAGE_0_DONE_PCT:     UpdateFieldsType.INT32,
    UpdateFieldPlayer.MOD_DAMAGE_1_DONE_PCT:     UpdateFieldsType.INT32,
    UpdateFieldPlayer.MOD_DAMAGE_2_DONE_PCT:     UpdateFieldsType.INT32,
    UpdateFieldPlayer.MOD_DAMAGE_3_DONE_PCT:     UpdateFieldsType.INT32,
    UpdateFieldPlayer.MOD_DAMAGE_4_DONE_PCT:     UpdateFieldsType.INT32,
    UpdateFieldPlayer.MOD_DAMAGE_5_DONE_PCT:     UpdateFieldsType.INT32,
    UpdateFieldPlayer.MOD_DAMAGE_6_DONE_PCT:     UpdateFieldsType.INT32,

    UpdateFieldPlayer.BYTES_4:                   UpdateFieldsType.FOUR_BYTES,

    UpdateFieldPlayer.AMMO_ID:                   UpdateFieldsType.INT32,

    UpdateFieldPlayer.PVP_MEDALS:                UpdateFieldsType.INT32,

    UpdateFieldPlayer.BUYBACK_ITEM_ID:           UpdateFieldsType.INT32,
    UpdateFieldPlayer.BUYBACK_RANDOM_PROP_ID:    UpdateFieldsType.INT32,
    UpdateFieldPlayer.BUYBACK_SEED:              UpdateFieldsType.INT32,
    UpdateFieldPlayer.BUYBACK_PRICE:             UpdateFieldsType.INT32,

    # --------------------
    # Game object fields
    # --------------------

    UpdateFieldGameObject.DISPLAY_ID: UpdateFieldsType.INT32,
    UpdateFieldGameObject.FLAGS:      UpdateFieldsType.INT32,

    UpdateFieldGameObject.ROTATION_1: UpdateFieldsType.FLOAT,
    UpdateFieldGameObject.ROTATION_2: UpdateFieldsType.FLOAT,
    UpdateFieldGameObject.ROTATION_3: UpdateFieldsType.FLOAT,
    UpdateFieldGameObject.ROTATION_4: UpdateFieldsType.FLOAT,

    UpdateFieldGameObject.STATE:      UpdateFieldsType.INT32,
    UpdateFieldGameObject.TIMESTAMP:  UpdateFieldsType.INT32,

    UpdateFieldGameObject.POS_X:      UpdateFieldsType.FLOAT,
    UpdateFieldGameObject.POS_Y:      UpdateFieldsType.FLOAT,
    UpdateFieldGameObject.POS_Z:      UpdateFieldsType.FLOAT,
    UpdateFieldGameObject.FACING:     UpdateFieldsType.FLOAT,

    UpdateFieldGameObject.DYN_FLAGS:  UpdateFieldsType.INT32,
    UpdateFieldGameObject.FACTION:    UpdateFieldsType.INT32,
    UpdateFieldGameObject.TYPE_ID:    UpdateFieldsType.INT32,
    UpdateFieldGameObject.LEVEL:      UpdateFieldsType.INT32,

    # --------------------
    # Dynamic object fields
    # --------------------

    UpdateFieldDynamicObject.CASTER:   UpdateFieldsType.INT64,
    UpdateFieldDynamicObject.BYTES:    UpdateFieldsType.FOUR_BYTES,
    UpdateFieldDynamicObject.SPELL_ID: UpdateFieldsType.INT32,
    UpdateFieldDynamicObject.RADIUS:   UpdateFieldsType.FLOAT,

    UpdateFieldDynamicObject.POS_X:    UpdateFieldsType.FLOAT,
    UpdateFieldDynamicObject.POS_Y:    UpdateFieldsType.FLOAT,
    UpdateFieldDynamicObject.POS_Z:    UpdateFieldsType.FLOAT,
    UpdateFieldDynamicObject.FACING:   UpdateFieldsType.FLOAT,

    # --------------------
    # Corpse fields
    # --------------------

    UpdateFieldCorpse.OWNER:      UpdateFieldsType.INT64,

    UpdateFieldCorpse.FACING:     UpdateFieldsType.FLOAT,
    UpdateFieldCorpse.POS_X:      UpdateFieldsType.FLOAT,
    UpdateFieldCorpse.POS_Y:      UpdateFieldsType.FLOAT,
    UpdateFieldCorpse.POS_Z:      UpdateFieldsType.FLOAT,

    UpdateFieldCorpse.DISPLAY_ID: UpdateFieldsType.INT32,

    UpdateFieldCorpse.ITEM_1:     UpdateFieldsType.INT32,
    UpdateFieldCorpse.ITEM_2:     UpdateFieldsType.INT32,
    UpdateFieldCorpse.ITEM_3:     UpdateFieldsType.INT32,
    UpdateFieldCorpse.ITEM_4:     UpdateFieldsType.INT32,
    UpdateFieldCorpse.ITEM_5:     UpdateFieldsType.INT32,
    UpdateFieldCorpse.ITEM_6:     UpdateFieldsType.INT32,
    UpdateFieldCorpse.ITEM_7:     UpdateFieldsType.INT32,
    UpdateFieldCorpse.ITEM_8:     UpdateFieldsType.INT32,
    UpdateFieldCorpse.ITEM_9:     UpdateFieldsType.INT32,
    UpdateFieldCorpse.ITEM_10:    UpdateFieldsType.INT32,
    UpdateFieldCorpse.ITEM_11:    UpdateFieldsType.INT32,
    UpdateFieldCorpse.ITEM_12:    UpdateFieldsType.INT32,
    UpdateFieldCorpse.ITEM_13:    UpdateFieldsType.INT32,
    UpdateFieldCorpse.ITEM_14:    UpdateFieldsType.INT32,
    UpdateFieldCorpse.ITEM_15:    UpdateFieldsType.INT32,
    UpdateFieldCorpse.ITEM_16:    UpdateFieldsType.INT32,
    UpdateFieldCorpse.ITEM_17:    UpdateFieldsType.INT32,
    UpdateFieldCorpse.ITEM_18:    UpdateFieldsType.INT32,
    UpdateFieldCorpse.ITEM_19:    UpdateFieldsType.INT32,

    UpdateFieldCorpse.BYTES_1:    UpdateFieldsType.FOUR_BYTES,
    UpdateFieldCorpse.BYTES_2:    UpdateFieldsType.FOUR_BYTES,

    UpdateFieldCorpse.GUILD:      UpdateFieldsType.INT32,
    UpdateFieldCorpse.FLAGS:      UpdateFieldsType.INT32
}
