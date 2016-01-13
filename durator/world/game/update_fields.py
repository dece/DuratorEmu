""" Update fields values used for build 4125, directly from the binary. """

from enum import Enum


class UpdateFieldObject(Enum):
    """ Hard limit: 0x6 """

    GUID    = 0x0
    TYPE    = 0x2
    ENTRY   = 0x3
    SCALE_X = 0x4

    PADDING = 0x5


class UpdateFieldItem(Enum):
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


class UpdateFieldContainer(Enum):
    """ Hard limit: 0x5A """

    NUM_SLOTS = 0x30 + 0x0
    PADDING   = 0x30 + 0x1
    SLOT_1    = 0x30 + 0x2  # 0x28 slots max, int64


class UpdateFieldUnit(Enum):
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


class UpdateFieldPlayer(Enum):
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

    SKILL_INFO_1_1              = 0xB0 + 0xA0   # 0x180 blocks

    QUEST_LOG_1_1               = 0xB0 + 0x220
    QUEST_LOG_1_2               = 0xB0 + 0x221
    QUEST_LOG_1_3               = 0xB0 + 0x222
    QUEST_LOG_2_1               = 0xB0 + 0x223
    QUEST_LOG_2_2               = 0xB0 + 0x224
    QUEST_LOG_2_3               = 0xB0 + 0x225
    QUEST_LOG_3_1               = 0xB0 + 0x226
    QUEST_LOG_3_2               = 0xB0 + 0x227
    QUEST_LOG_3_3               = 0xB0 + 0x228
    QUEST_LOG_4_1               = 0xB0 + 0x229
    QUEST_LOG_4_2               = 0xB0 + 0x22A
    QUEST_LOG_4_3               = 0xB0 + 0x22B
    QUEST_LOG_5_1               = 0xB0 + 0x22C
    QUEST_LOG_5_2               = 0xB0 + 0x22D
    QUEST_LOG_5_3               = 0xB0 + 0x22E
    QUEST_LOG_6_1               = 0xB0 + 0x22F
    QUEST_LOG_6_2               = 0xB0 + 0x230
    QUEST_LOG_6_3               = 0xB0 + 0x231
    QUEST_LOG_7_1               = 0xB0 + 0x232
    QUEST_LOG_7_2               = 0xB0 + 0x233
    QUEST_LOG_7_3               = 0xB0 + 0x234
    QUEST_LOG_8_1               = 0xB0 + 0x235
    QUEST_LOG_8_2               = 0xB0 + 0x236
    QUEST_LOG_8_3               = 0xB0 + 0x237
    QUEST_LOG_9_1               = 0xB0 + 0x238
    QUEST_LOG_9_2               = 0xB0 + 0x239
    QUEST_LOG_9_3               = 0xB0 + 0x23A
    QUEST_LOG_10_1              = 0xB0 + 0x23B
    QUEST_LOG_10_2              = 0xB0 + 0x23C
    QUEST_LOG_10_3              = 0xB0 + 0x23D
    QUEST_LOG_11_1              = 0xB0 + 0x23E
    QUEST_LOG_11_2              = 0xB0 + 0x23F
    QUEST_LOG_11_3              = 0xB0 + 0x240
    QUEST_LOG_12_1              = 0xB0 + 0x241
    QUEST_LOG_12_2              = 0xB0 + 0x242
    QUEST_LOG_12_3              = 0xB0 + 0x243
    QUEST_LOG_13_1              = 0xB0 + 0x244
    QUEST_LOG_13_2              = 0xB0 + 0x245
    QUEST_LOG_13_3              = 0xB0 + 0x246
    QUEST_LOG_14_1              = 0xB0 + 0x247
    QUEST_LOG_14_2              = 0xB0 + 0x248
    QUEST_LOG_14_3              = 0xB0 + 0x249
    QUEST_LOG_15_1              = 0xB0 + 0x24A
    QUEST_LOG_15_2              = 0xB0 + 0x24B
    QUEST_LOG_15_3              = 0xB0 + 0x24C
    QUEST_LOG_16_1              = 0xB0 + 0x24D
    QUEST_LOG_16_2              = 0xB0 + 0x24E
    QUEST_LOG_16_3              = 0xB0 + 0x24F
    QUEST_LOG_17_1              = 0xB0 + 0x250
    QUEST_LOG_17_2              = 0xB0 + 0x251
    QUEST_LOG_17_3              = 0xB0 + 0x252
    QUEST_LOG_18_1              = 0xB0 + 0x253
    QUEST_LOG_18_2              = 0xB0 + 0x254
    QUEST_LOG_18_3              = 0xB0 + 0x255
    QUEST_LOG_19_1              = 0xB0 + 0x256
    QUEST_LOG_19_2              = 0xB0 + 0x257
    QUEST_LOG_19_3              = 0xB0 + 0x258
    QUEST_LOG_20_1              = 0xB0 + 0x259
    QUEST_LOG_20_2              = 0xB0 + 0x25A
    QUEST_LOG_20_3              = 0xB0 + 0x25B

    CHARACTER_POINTS_1          = 0xB0 + 0x25C
    CHARACTER_POINTS_2          = 0xB0 + 0x25D  # professions left?

    TRACK_CREATURES             = 0xB0 + 0x25E
    TRACK_RESOURCES             = 0xB0 + 0x25F

    CHAT_FILTERS                = 0xB0 + 0x260

    BLOCK_PERCENTAGE            = 0xB0 + 0x261
    DODGE_PERCENTAGE            = 0xB0 + 0x262
    PARRY_PERCENTAGE            = 0xB0 + 0x263
    CRIT_PERCENTAGE             = 0xB0 + 0x264

    EXPLORED_ZONES_1            = 0xB0 + 0x265
    EXPLORED_ZONES_2            = 0xB0 + 0x266
    EXPLORED_ZONES_3            = 0xB0 + 0x267
    EXPLORED_ZONES_4            = 0xB0 + 0x268
    EXPLORED_ZONES_5            = 0xB0 + 0x269
    EXPLORED_ZONES_6            = 0xB0 + 0x26A
    EXPLORED_ZONES_7            = 0xB0 + 0x26B
    EXPLORED_ZONES_8            = 0xB0 + 0x26C
    EXPLORED_ZONES_9            = 0xB0 + 0x26D
    EXPLORED_ZONES_10           = 0xB0 + 0x26E
    EXPLORED_ZONES_11           = 0xB0 + 0x26F
    EXPLORED_ZONES_12           = 0xB0 + 0x270
    EXPLORED_ZONES_13           = 0xB0 + 0x271
    EXPLORED_ZONES_14           = 0xB0 + 0x272
    EXPLORED_ZONES_15           = 0xB0 + 0x273
    EXPLORED_ZONES_16           = 0xB0 + 0x274
    EXPLORED_ZONES_17           = 0xB0 + 0x275
    EXPLORED_ZONES_18           = 0xB0 + 0x276
    EXPLORED_ZONES_19           = 0xB0 + 0x277
    EXPLORED_ZONES_20           = 0xB0 + 0x278
    EXPLORED_ZONES_21           = 0xB0 + 0x279
    EXPLORED_ZONES_22           = 0xB0 + 0x27A
    EXPLORED_ZONES_23           = 0xB0 + 0x27B
    EXPLORED_ZONES_24           = 0xB0 + 0x27C
    EXPLORED_ZONES_25           = 0xB0 + 0x27D
    EXPLORED_ZONES_26           = 0xB0 + 0x27E
    EXPLORED_ZONES_27           = 0xB0 + 0x27F
    EXPLORED_ZONES_28           = 0xB0 + 0x280
    EXPLORED_ZONES_29           = 0xB0 + 0x281
    EXPLORED_ZONES_30           = 0xB0 + 0x282
    EXPLORED_ZONES_31           = 0xB0 + 0x283
    EXPLORED_ZONES_32           = 0xB0 + 0x284

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


class UpdateFieldGameObject(Enum):
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


class UpdateFieldDynamicObject(Enum):
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


class UpdateFieldCorpse(Enum):
    """ Hard limit: 0x24 """

    OWNER         = 0x6 + 0x0

    FACING        = 0x6 + 0x2
    POS_X         = 0x6 + 0x3
    POS_Y         = 0x6 + 0x4
    POS_Z         = 0x6 + 0x5

    DISPLAY_ID    = 0x6 + 0x6

    ITEM_1        = 0x6 + 0x7
    ITEM_2        = 0x6 + 0x8
    ITEM_3        = 0x6 + 0x9
    ITEM_4        = 0x6 + 0xA
    ITEM_5        = 0x6 + 0xB
    ITEM_6        = 0x6 + 0xC
    ITEM_7        = 0x6 + 0xD
    ITEM_8        = 0x6 + 0xE
    ITEM_9        = 0x6 + 0xF
    ITEM_10       = 0x6 + 0x10
    ITEM_11       = 0x6 + 0x11
    ITEM_12       = 0x6 + 0x12
    ITEM_13       = 0x6 + 0x13
    ITEM_14       = 0x6 + 0x14
    ITEM_15       = 0x6 + 0x15
    ITEM_16       = 0x6 + 0x16
    ITEM_17       = 0x6 + 0x17
    ITEM_18       = 0x6 + 0x18
    ITEM_19       = 0x6 + 0x19

    BYTES_1       = 0x6 + 0x1A
    BYTES_2       = 0x6 + 0x1B

    GUILD         = 0x6 + 0x1C
    FLAGS         = 0x6 + 0x1D
