from enum import Enum
import math
from struct import Struct

from durator.db.database import db_connection
from durator.world.character import Character
from durator.world.opcodes import OpCode
from durator.world.world_connection_state import WorldConnectionState
from durator.world.world_packet import WorldPacket
from pyshgck.logger import LOG


class UpdateType(Enum):
    """ Determine the UpdateObject packet format. """

    PARTIAL       = 0  # to be confirmed / renamed
    MOVEMENT      = 1
    CREATE_OBJECT = 2
    FAR_OBJECTS   = 3
    NEAR_OBJECTS  = 4


class ObjectType(Enum):
    """ Object type sent in UpdateObject packets, with associated flags. """

    OBJECT         = 0  # 0x01 (object)
    ITEM           = 1  # 0x03 (object, item)
    CONTAINER      = 2  # 0x07 (object, item, container)
    UNIT           = 3  # 0x09 (object, unit)
    PLAYER         = 4  # 0x19 (object, unit, player)
    GAME_OBJECT    = 5  # 0x21 (object, game_object)
    DYNAMIC_OBJECT = 6  # 0x41 (object, dynamic_object)
    CORPSE         = 7  # 0x81 (object, corpse)


class ObjectDescFlags(Enum):
    """ BaseObject descriptors "flags" (field 0x8). """

    OBJECT         = 1 << 0
    ITEM           = 1 << 1
    CONTAINER      = 1 << 2
    UNIT           = 1 << 3
    PLAYER         = 1 << 4
    GAME_OBJECT    = 1 << 5
    DYNAMIC_OBJECT = 1 << 6
    CORPSE         = 1 << 7








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
    MAX_POWER_5               = 0x6 + 0xAB

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

    BYTES_1                     = 0xB0 + 0x7  # originally "BYTES"
    BYTES_2                     = 0xB0 + 0x8
    BYTES_3                     = 0xB0 + 0x9

    DUEL_TEAM                   = 0xB0 + 0xA
    GUILD_TIMESTAMP             = 0xB0 + 0xB

    INV_SLOT_HEAD               = 0xB0 + 0xC   # 0x2E blocks, int64

    PACK_SLOT_1                 = 0xB0 + 0x3A  # 0x20 blocks, int64

    BANK_SLOT_1                 = 0xB0 + 0x5A  # 0x30 blocks, int64

    BANK_BAG_SLOT_1             = 0xB0 + 0x8A  # 0x0C blocks, int64

    VENDOR_BUY_BACK_SLOT        = 0xB0 + 0x96

    FAR_SIGHT                   = 0xB0 + 0x98
    COMBO_TARGET                = 0xB0 + 0x9A

    BUY_BACK_NPC                = 0xB0 + 0x9C

    EXP                         = 0xB0 + 0x9E
    NEXT_LEVEL_XP               = 0xB0 + 0x9F

    SKILL_INFO_1_1              = 0xB0 + 0xA0  # 0x180 blocks

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

    REST_STATE_EXPERIENCE       = 0xB0 + 0x285
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


class ObjectUpdate(object):

    FIELD_BIN_MAP = {
        UpdateFieldsType.INT32:      Struct("<i"),
        UpdateFieldsType.TWO_INT16:  Struct("<I"),
        UpdateFieldsType.FLOAT:      Struct("<f"),
        UpdateFieldsType.INT64:      Struct("<q"),
        UpdateFieldsType.FOUR_BYTES: Struct("<I")
    }

    def __init__(self):
        self.mask_blocks = []
        self.update_blocks = []

    def add(self, field, value):
        try:
            field_type = UPDATE_FIELD_TYPE_MAP[field]
        except KeyError:
            LOG.error("No type associated with " + str(field))
            LOG.error("Object not updated.")
            return

        field_struct = self.FIELD_BIN_MAP[field_type]
        self._set_field_mask_bits(field, field_struct)

        update_block = field_struct.pack(value)
        self.update_blocks.append(update_block)

    def _set_field_mask_bits(self, field, field_struct):
        num_mask_blocks = math.ceil(field_struct.size / 4)
        for field_value in range(field.value, field.value + num_mask_blocks):
            self._set_field_mask_bit(field_value)

    def _set_field_mask_bit(self, field_value):
        mask_block_index = field_value // 32
        bit_index = field_value % 32
        while len(self.mask_blocks) < mask_block_index+1:
            self.mask_blocks.append(0)
        self.mask_blocks[mask_block_index] |= 1 << bit_index

    def to_bytes(self):
        mask = b"".join(
            [int.to_bytes(block, 4, "little") for block in self.mask_blocks]
        )
        update_data = b"".join(
            self.update_blocks
        )
        return mask + update_data




class PlayerLoginHandler(object):
    """ Handle the player entering in world. """

    # We should answer with a validation and a few more informations. Some
    # things that are sent to the client right after on Mangos Classic are:
    # - send server message of the day
    # - send guild message of the day
    # - check if character is dead, then send corpse reclaim timer
    # - set the rest value
    # - set the homebind
    # - possibly send cinematic if it's a first login
    # - set time speed
    # - maybe teleport player back to his homebind
    # - send friend and ignore list
    # - send stuff like water walk, etc
    # - possibly send server imminent shutdown notice

    PACKET_BIN = Struct("<Q")
    WORLD_INFO_BIN = Struct("<I4f")

    def __init__(self, connection, packet):
        self.conn = connection
        self.packet = packet

    @db_connection
    def process(self):
        self.conn.guid = self.PACKET_BIN.unpack(self.packet)[0]
        self.conn.character = self._get_checked_character()
        if self.conn.character is None:
            LOG.warning("Account {} tried to illegally use character {}".format(
                self.conn.account.name, self.conn.guid
            ))
            return self.conn.MAIN_ERROR_STATE, None

        self.conn.send_packet(self._get_verify_login_packet())
        self.conn.send_packet(self._get_new_world_packet())
        self.conn.temp_data["worldport_ack_pending"] = True
        self.conn.send_packet(self._get_update_object_packet())

        return WorldConnectionState.IN_WORLD, None

    def _get_checked_character(self):
        """ Set the connection character to the specified GUID only if this
        character belongs to the connected account, to avoid illegal uses. """
        try:
            character = Character.get(
                Character.guid == self.conn.guid
                and Character.account == self.conn.account
            )
            return character
        except Character.DoesNotExist:
            return None

    def _get_verify_login_packet(self):
        position = self.conn.character.position
        response_data = self.WORLD_INFO_BIN.pack(
            position.map_id,
            position.pos_x,
            position.pos_y,
            position.pos_z,
            position.orientation
        )

        packet = WorldPacket(response_data)
        packet.opcode = OpCode.SMSG_LOGIN_VERIFY_WORLD
        return packet

    def _get_new_world_packet(self):
        position = self.conn.character.position
        response_data = self.WORLD_INFO_BIN.pack(
            position.map_id,
            position.pos_x,
            position.pos_y,
            position.pos_z,
            position.orientation
        )

        packet = WorldPacket(response_data)
        packet.opcode = OpCode.SMSG_NEW_WORLD
        return packet


    UPDATE_PART1_BIN    = Struct("<I2BQB")
    UPDATE_MOVEMENT_BIN = Struct("<2I4f6f")
    UPDATE_PART2_BIN    = Struct("<3IQ")

    def _get_update_object_packet(self):
        """ Copy pasted stuff from WoWCore, with a few adaptations for 1.1 """
        char = self.conn.character
        race = char.race
        class_id = char.class_id
        gender = char.gender
        
        position = char.position

        # guid_mask, guid_bytes = _pack_guid(self.conn.guid)
        # packed_guid = int.to_bytes(guid_mask, 1, "little") + guid_bytes

        data = b""
        data += self.UPDATE_PART1_BIN.pack(
            1,  # count
            0,  # has transport?
            UpdateType.CREATE_OBJECT.value,  # update type
            self.conn.guid,
            ObjectType.PLAYER.value  # object type
        )
        data += self.UPDATE_MOVEMENT_BIN.pack(
            0,  # movement flags
            0,  # unk?
            position.pos_x,
            position.pos_y,
            position.pos_z,
            position.orientation,
            2.5,  # walkspeed
            7.0,  # runningspeed
            2.5,  # runbackspeed
            4.7222223,  # swimspeed
            4.0,  # swimbackspeed
            3.141593  # turnrate
        )
        data += self.UPDATE_PART2_BIN.pack(
            1,  # is player?
            1,  # attack cycle
            0,  # timer id
            0   # victim GUID
        )

        update = ObjectUpdate()
        update.add(UpdateFieldObject.GUID, self.conn.guid)
        update.add(UpdateFieldObject.TYPE, ( ObjectDescFlags.OBJECT.value |
                                             ObjectDescFlags.UNIT.value |
                                             ObjectDescFlags.PLAYER.value ) )
        update.add(UpdateFieldObject.SCALE_X, 1.0)

        update.add(UpdateFieldUnit.HEALTH, 100)
        update.add(UpdateFieldUnit.POWER_1, 100)
        update.add(UpdateFieldUnit.POWER_2, 100)
        update.add(UpdateFieldUnit.POWER_3, 100)
        update.add(UpdateFieldUnit.POWER_4, 100)
        update.add(UpdateFieldUnit.POWER_5, 100)
        update.add(UpdateFieldUnit.MAX_HEALTH, 100)
        update.add(UpdateFieldUnit.MAX_POWER_1, 100)
        update.add(UpdateFieldUnit.MAX_POWER_2, 100)
        update.add(UpdateFieldUnit.MAX_POWER_3, 100)
        update.add(UpdateFieldUnit.MAX_POWER_4, 100)
        update.add(UpdateFieldUnit.MAX_POWER_5, 100)

        update.add(UpdateFieldUnit.LEVEL, 1)
        update.add(UpdateFieldUnit.FACTION_TEMPLATE, 35)  # or 5 for undead?
        update.add(UpdateFieldUnit.BYTES_0, ( race | (class_id << 8) |
                                              (gender << 16) | (1 << 24) ) )
        update.add(UpdateFieldUnit.FLAGS, 0)

        update.add(UpdateFieldUnit.BASE_ATTACK_TIME, 2000)
        update.add(UpdateFieldUnit.OFFHAND_ATTACK_TIME, 2000)

        update.add(UpdateFieldUnit.BOUNDING_RADIUS, 0.382999)  # undead values
        update.add(UpdateFieldUnit.COMBAT_REACH, 1.500000)

        update.add(UpdateFieldUnit.DISPLAY_ID, 57)
        update.add(UpdateFieldUnit.NATIVE_DISPLAY_ID, 57)
        update.add(UpdateFieldUnit.MOUNT_DISPLAY_ID, 0)

        update.add(UpdateFieldUnit.MIN_DAMAGE, 0)
        update.add(UpdateFieldUnit.MAX_DAMAGE, 0)
        update.add(UpdateFieldUnit.MIN_OFFHAND_DAMAGE, 0)
        update.add(UpdateFieldUnit.MAX_OFFHAND_DAMAGE, 0)

        update.add(UpdateFieldUnit.BYTES_1, 0)  # stand state and stuff

        update.add(UpdateFieldUnit.MOD_CAST_SPEED, 1)

        update.add(UpdateFieldUnit.STAT_0, 0)
        update.add(UpdateFieldUnit.STAT_1, 1)
        update.add(UpdateFieldUnit.STAT_2, 2)
        update.add(UpdateFieldUnit.STAT_3, 3)
        update.add(UpdateFieldUnit.STAT_4, 4)

        update.add(UpdateFieldUnit.RESISTANCE_0, 0)
        update.add(UpdateFieldUnit.RESISTANCE_1, 1)
        update.add(UpdateFieldUnit.RESISTANCE_2, 2)
        update.add(UpdateFieldUnit.RESISTANCE_3, 3)
        update.add(UpdateFieldUnit.RESISTANCE_4, 4)
        update.add(UpdateFieldUnit.RESISTANCE_5, 5)

        update.add(UpdateFieldUnit.BASE_MANA, 1)

        update.add(UpdateFieldUnit.BYTES_2, 0)  # weapons sheathed and stuff

        update.add(UpdateFieldUnit.ATTACK_POWER, 0)
        update.add(UpdateFieldUnit.ATTACK_POWER_MODS, 0)
        update.add(UpdateFieldUnit.RANGED_ATTACK_POWER, 0)
        update.add(UpdateFieldUnit.RANGED_ATTACK_POWER_MODS, 0)

        update.add(UpdateFieldUnit.MIN_RANGED_DAMAGE, 0)
        update.add(UpdateFieldUnit.MAX_RANGED_DAMAGE, 0)

        features = char.features

        update.add(UpdateFieldPlayer.FLAGS, 0)

        player_bytes_1 = ( features.skin |
                           features.face << 8 |
                           features.hair_style << 16 |
                           features.hair_color << 24 )
        player_bytes_2 = ( features.facial_hair |
                           1 << 24 )  # restInfo
        player_bytes_3 = gender

        update.add(UpdateFieldPlayer.BYTES_1, player_bytes_1)
        update.add(UpdateFieldPlayer.BYTES_2, player_bytes_2)
        update.add(UpdateFieldPlayer.BYTES_3, player_bytes_3)

        update.add(UpdateFieldPlayer.EXP, 100)
        update.add(UpdateFieldPlayer.NEXT_LEVEL_XP, 2500)

        update.add(UpdateFieldPlayer.CHARACTER_POINTS_1, 0)
        update.add(UpdateFieldPlayer.CHARACTER_POINTS_2, 2)

        update.add(UpdateFieldPlayer.BLOCK_PERCENTAGE, 4.0)
        update.add(UpdateFieldPlayer.DODGE_PERCENTAGE, 4.0)
        update.add(UpdateFieldPlayer.PARRY_PERCENTAGE, 4.0)
        update.add(UpdateFieldPlayer.CRIT_PERCENTAGE, 4.0)

        update.add(UpdateFieldPlayer.REST_STATE_EXPERIENCE, 200)
        update.add(UpdateFieldPlayer.COINAGE, 1230000)




        # update mask block count, hard limit at 1C
        num_mask_blocks = len(update.mask_blocks)
        if num_mask_blocks >= 0x1C:
            LOG.critical( "Too much update mask blocks ({:X}), "
                          "you probably fucked up something".format(
                num_mask_blocks
            ))
            raise Exception()
        data += int.to_bytes(num_mask_blocks, 1, "little")

        data += update.to_bytes()

        packet = WorldPacket(data)
        packet.opcode = OpCode.SMSG_UPDATE_OBJECT
        return packet
