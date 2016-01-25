""" Update fields values used for build 4125, directly from the binary. """

from enum import Enum


class ObjectField(Enum):
    """ Hard limit: 0x6 """

    GUID    = 0x0
    TYPE    = 0x2
    ENTRY   = 0x3
    SCALE_X = 0x4

    PADDING = 0x5


class ItemField(Enum):
    """ Hard limit: 0x30 """

    OWNER                = 0x6 + 0x0
    CONTAINED            = 0x6 + 0x2
    CREATOR              = 0x6 + 0x4
    GIFTCREATOR          = 0x6 + 0x6

    STACK_COUNT          = 0x6 + 0x8
    DURATION             = 0x6 + 0x9
    SPELL_CHARGES        = 0x6 + 0xA

    FLAGS                = 0x6 + 0xF

    ENCHANTMENT          = 0x6 + 0x10

    PROPERTY_SEED        = 0x6 + 0x25
    RANDOM_PROPERTIES_ID = 0x6 + 0x26
    ITEM_TEXT_ID         = 0x6 + 0x27

    DURABILITY           = 0x6 + 0x28
    MAX_DURABILITY       = 0x6 + 0x29


class ContainerField(Enum):
    """ Hard limit: 0x5A """

    NUM_SLOTS = 0x30 + 0x0
    PADDING   = 0x30 + 0x1
    SLOT_1    = 0x30 + 0x2  # 0x28 slots max, int64


class UnitField(Enum):
    """ Hard limit: 0xB0 """

    CHARM                     = 0x6 + 0x0
    SUMMON                    = 0x6 + 0x2
    CHARMED_BY                = 0x6 + 0x4
    SUMMONED_BY               = 0x6 + 0x6
    CREATED_BY                = 0x6 + 0x8
    TARGET                    = 0x6 + 0xA
    PERSUADED                 = 0x6 + 0xC
    CHANNEL_OBJECT            = 0x6 + 0xE

    HEALTH                    = 0x6 + 0x10
    POWER_1                   = 0x6 + 0x11
    POWER_2                   = 0x6 + 0x12
    POWER_3                   = 0x6 + 0x13
    POWER_4                   = 0x6 + 0x14
    POWER_5                   = 0x6 + 0x15

    MAX_HEALTH                = 0x6 + 0x16
    MAX_POWER_1               = 0x6 + 0x17
    MAX_POWER_2               = 0x6 + 0x18
    MAX_POWER_3               = 0x6 + 0x19
    MAX_POWER_4               = 0x6 + 0x1A
    MAX_POWER_5               = 0x6 + 0x1B

    LEVEL                     = 0x6 + 0x1C
    FACTION_TEMPLATE          = 0x6 + 0x1D
    BYTES_0                   = 0x6 + 0x1E
    VIRTUAL_ITEM_SLOT_DISPLAY = 0x6 + 0x1F
    VIRTUAL_ITEM_INFO         = 0x6 + 0x22
    FLAGS                     = 0x6 + 0x28

    AURA                      = 0x6 + 0x29
    AURA_LEVELS               = 0x6 + 0x61
    AURA_APPLICATIONS         = 0x6 + 0x6B
    AURA_FLAGS                = 0x6 + 0x75
    AURA_STATE                = 0x6 + 0x7C

    BASE_ATTACK_TIME          = 0x6 + 0x7D
    OFFHAND_ATTACK_TIME       = 0x6 + 0x7E
    RANGED_ATTACK_TIME        = 0x6 + 0x7F

    BOUNDING_RADIUS           = 0x6 + 0x80
    COMBAT_REACH              = 0x6 + 0x81

    DISPLAY_ID                = 0x6 + 0x82
    NATIVE_DISPLAY_ID         = 0x6 + 0x83
    MOUNT_DISPLAY_ID          = 0x6 + 0x84

    MIN_DAMAGE                = 0x6 + 0x85
    MAX_DAMAGE                = 0x6 + 0x86
    MIN_OFFHAND_DAMAGE        = 0x6 + 0x87
    MAX_OFFHAND_DAMAGE        = 0x6 + 0x88

    BYTES_1                   = 0x6 + 0x89

    PET_NUMBER                = 0x6 + 0x8A
    PET_NAME_TIMESTAMP        = 0x6 + 0x8B
    PET_EXPERIENCE            = 0x6 + 0x8C
    PET_NEXT_LEVEL_EXP        = 0x6 + 0x8D

    DYNAMIC_FLAGS             = 0x6 + 0x8E
    CHANNEL_SPELL             = 0x6 + 0x8F
    MOD_CAST_SPEED            = 0x6 + 0x90
    CREATED_BY_SPELL          = 0x6 + 0x91

    NPC_FLAGS                 = 0x6 + 0x92
    NPC_EMOTESTATE            = 0x6 + 0x93

    TRAINING_POINTS           = 0x6 + 0x94

    STAT_0                    = 0x6 + 0x95
    STAT_1                    = 0x6 + 0x96
    STAT_2                    = 0x6 + 0x97
    STAT_3                    = 0x6 + 0x98
    STAT_4                    = 0x6 + 0x99
    RESISTANCE_0              = 0x6 + 0x9A
    RESISTANCE_1              = 0x6 + 0x9B
    RESISTANCE_2              = 0x6 + 0x9C
    RESISTANCE_3              = 0x6 + 0x9D
    RESISTANCE_4              = 0x6 + 0x9E
    RESISTANCE_5              = 0x6 + 0x9F
    RESISTANCE_6              = 0x6 + 0xA0

    ATTACK_POWER              = 0x6 + 0xA1
    BASE_MANA                 = 0x6 + 0xA2
    ATTACK_POWER_MODS         = 0x6 + 0xA3

    BYTES_2                   = 0x6 + 0xA4

    RANGED_ATTACK_POWER       = 0x6 + 0xA5
    RANGED_ATTACK_POWER_MODS  = 0x6 + 0xA6
    MIN_RANGED_DAMAGE         = 0x6 + 0xA7
    MAX_RANGED_DAMAGE         = 0x6 + 0xA8

    PADDING                   = 0x6 + 0xA9


class PlayerField(Enum):
    """ Hard limit: 0x36C """

    SELECTION                   = 0xB0 + 0x0
    DUEL_ARBITER                = 0xB0 + 0x2
    FLAGS                       = 0xB0 + 0x4

    GUILD_ID                    = 0xB0 + 0x5
    GUILD_RANK                  = 0xB0 + 0x6

    BYTES_1                     = 0xB0 + 0x7    # originally "BYTES"
    BYTES_2                     = 0xB0 + 0x8
    BYTES_3                     = 0xB0 + 0x9

    DUEL_TEAM                   = 0xB0 + 0xA
    GUILD_TIMESTAMP             = 0xB0 + 0xB

    INV_SLOT_HEAD               = 0xB0 + 0xC    # 0x2E blocks, int64

    PACK_SLOT_1                 = 0xB0 + 0x3A   # 0x20 blocks, int64

    BANK_SLOT_1                 = 0xB0 + 0x5A   # 0x30 blocks, int64

    BANK_BAG_SLOT_1             = 0xB0 + 0x8A   # 0x0C blocks, int64

    VENDOR_BUY_BACK_SLOT        = 0xB0 + 0x96

    FAR_SIGHT                   = 0xB0 + 0x98
    COMBO_TARGET                = 0xB0 + 0x9A

    BUY_BACK_NPC                = 0xB0 + 0x9C

    EXP                         = 0xB0 + 0x9E
    NEXT_LEVEL_EXP              = 0xB0 + 0x9F

    SKILL_INFO_1_ID             = 0xB0 + 0xA0   # 128 skills (NUM_SKILLS)
    SKILL_INFO_1_LEVEL          = 0xB0 + 0xA1   # 3 entries per skill
    SKILL_INFO_1_STAT_LEVEL     = 0xB0 + 0xA2   # access directly by value

    QUEST_LOG_1_1               = 0xB0 + 0x220  # 20 quest logs
    QUEST_LOG_1_2               = 0xB0 + 0x221  # access directly by value
    QUEST_LOG_1_3               = 0xB0 + 0x222

    CHARACTER_POINTS_1          = 0xB0 + 0x25C
    CHARACTER_POINTS_2          = 0xB0 + 0x25D  # professions left?

    TRACK_CREATURES             = 0xB0 + 0x25E
    TRACK_RESOURCES             = 0xB0 + 0x25F

    CHAT_FILTERS                = 0xB0 + 0x260

    BLOCK_PERCENTAGE            = 0xB0 + 0x261
    DODGE_PERCENTAGE            = 0xB0 + 0x262
    PARRY_PERCENTAGE            = 0xB0 + 0x263
    CRIT_PERCENTAGE             = 0xB0 + 0x264

    EXPLORED_ZONES_1            = 0xB0 + 0x265  # 32 zones

    REST_STATE_EXP              = 0xB0 + 0x285
    COINAGE                     = 0xB0 + 0x286

    POS_STAT_0                  = 0xB0 + 0x287
    POS_STAT_1                  = 0xB0 + 0x288
    POS_STAT_2                  = 0xB0 + 0x289
    POS_STAT_3                  = 0xB0 + 0x28A
    POS_STAT_4                  = 0xB0 + 0x28B
    NEG_STAT_0                  = 0xB0 + 0x28C
    NEG_STAT_1                  = 0xB0 + 0x28D
    NEG_STAT_2                  = 0xB0 + 0x28E
    NEG_STAT_3                  = 0xB0 + 0x28F
    NEG_STAT_4                  = 0xB0 + 0x290

    RESISTANCE_0_BUFF_MOD_POS   = 0xB0 + 0x291
    RESISTANCE_1_BUFF_MOD_POS   = 0xB0 + 0x292
    RESISTANCE_2_BUFF_MOD_POS   = 0xB0 + 0x293
    RESISTANCE_3_BUFF_MOD_POS   = 0xB0 + 0x294
    RESISTANCE_4_BUFF_MOD_POS   = 0xB0 + 0x295
    RESISTANCE_5_BUFF_MOD_POS   = 0xB0 + 0x296
    RESISTANCE_6_BUFF_MOD_POS   = 0xB0 + 0x297
    RESISTANCE_0_BUFF_MOD_NEG   = 0xB0 + 0x298
    RESISTANCE_1_BUFF_MOD_NEG   = 0xB0 + 0x299
    RESISTANCE_2_BUFF_MOD_NEG   = 0xB0 + 0x29A
    RESISTANCE_3_BUFF_MOD_NEG   = 0xB0 + 0x29B
    RESISTANCE_4_BUFF_MOD_NEG   = 0xB0 + 0x29C
    RESISTANCE_5_BUFF_MOD_NEG   = 0xB0 + 0x29D
    RESISTANCE_6_BUFF_MOD_NEG   = 0xB0 + 0x29E

    MOD_DAMAGE_0_DONE_POS       = 0xB0 + 0x29F
    MOD_DAMAGE_1_DONE_POS       = 0xB0 + 0x2A0
    MOD_DAMAGE_2_DONE_POS       = 0xB0 + 0x2A1
    MOD_DAMAGE_3_DONE_POS       = 0xB0 + 0x2A2
    MOD_DAMAGE_4_DONE_POS       = 0xB0 + 0x2A3
    MOD_DAMAGE_5_DONE_POS       = 0xB0 + 0x2A4
    MOD_DAMAGE_6_DONE_POS       = 0xB0 + 0x2A5
    MOD_DAMAGE_0_DONE_NEG       = 0xB0 + 0x2A6
    MOD_DAMAGE_1_DONE_NEG       = 0xB0 + 0x2A7
    MOD_DAMAGE_2_DONE_NEG       = 0xB0 + 0x2A8
    MOD_DAMAGE_3_DONE_NEG       = 0xB0 + 0x2A9
    MOD_DAMAGE_4_DONE_NEG       = 0xB0 + 0x2AA
    MOD_DAMAGE_5_DONE_NEG       = 0xB0 + 0x2AB
    MOD_DAMAGE_6_DONE_NEG       = 0xB0 + 0x2AC
    MOD_DAMAGE_0_DONE_PCT       = 0xB0 + 0x2AD
    MOD_DAMAGE_1_DONE_PCT       = 0xB0 + 0x2AE
    MOD_DAMAGE_2_DONE_PCT       = 0xB0 + 0x2AF
    MOD_DAMAGE_3_DONE_PCT       = 0xB0 + 0x2B0
    MOD_DAMAGE_4_DONE_PCT       = 0xB0 + 0x2B1
    MOD_DAMAGE_5_DONE_PCT       = 0xB0 + 0x2B2
    MOD_DAMAGE_6_DONE_PCT       = 0xB0 + 0x2B3

    BYTES_4                     = 0xB0 + 0x2B4  # originally "BYTES"

    AMMO_ID                     = 0xB0 + 0x2B5

    PVP_MEDALS                  = 0xB0 + 0x2B6

    BUYBACK_ITEM_ID             = 0xB0 + 0x2B7
    BUYBACK_RANDOM_PROP_ID      = 0xB0 + 0x2B8
    BUYBACK_SEED                = 0xB0 + 0x2B9
    BUYBACK_PRICE               = 0xB0 + 0x2BA

    PADDING                     = 0xB0 + 0x2BB


class GameObjectField(Enum):
    """ Hard limit: 0x16 """

    DISPLAY_ID       = 0x6 + 0x0
    FLAGS            = 0x6 + 0x1

    ROTATION_1       = 0x6 + 0x2  # probably quats? it's floats
    ROTATION_2       = 0x6 + 0x3
    ROTATION_3       = 0x6 + 0x4
    ROTATION_4       = 0x6 + 0x5

    STATE            = 0x6 + 0x6
    TIMESTAMP        = 0x6 + 0x7

    POS_X            = 0x6 + 0x8
    POS_Y            = 0x6 + 0x9
    POS_Z            = 0x6 + 0xA
    FACING           = 0x6 + 0xB

    DYN_FLAGS        = 0x6 + 0xC
    FACTION          = 0x6 + 0xD
    TYPE_ID          = 0x6 + 0xE
    LEVEL            = 0x6 + 0xF


class DynamicObjectField(Enum):
    """ Hard limit: 0x10 """

    CASTER   = 0x6 + 0x0
    BYTES    = 0x6 + 0x2
    SPELL_ID = 0x6 + 0x3
    RADIUS   = 0x6 + 0x4

    POS_X    = 0x6 + 0x5
    POS_Y    = 0x6 + 0x6
    POS_Z    = 0x6 + 0x7
    FACING   = 0x6 + 0x8

    PADDING  = 0x6 + 0x9


class CorpseField(Enum):
    """ Hard limit: 0x24 """

    OWNER         = 0x6 + 0x0

    FACING        = 0x6 + 0x2
    POS_X         = 0x6 + 0x3
    POS_Y         = 0x6 + 0x4
    POS_Z         = 0x6 + 0x5

    DISPLAY_ID    = 0x6 + 0x6

    ITEM_1        = 0x6 + 0x7  # 19 items, access directly by value

    BYTES_1       = 0x6 + 0x1A
    BYTES_2       = 0x6 + 0x1B

    GUILD         = 0x6 + 0x1C
    FLAGS         = 0x6 + 0x1D
