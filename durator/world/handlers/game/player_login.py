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

    GUID    = 0
    TYPE    = 2
    ENTRY   = 3
    SCALE_X = 4
    PADDING = 5


class UpdateFieldItem(Enum):
    """ Hard limit: 0x30 """

    OWNER                = 6
    CONTAINED            = 8
    CREATOR              = 10
    GIFTCREATOR          = 12
    STACK_COUNT          = 14
    DURATION             = 15
    SPELL_CHARGES        = 16
    FLAGS                = 21
    ENCHANTMENT          = 22
    PROPERTY_SEED        = 43
    RANDOM_PROPERTIES_ID = 44
    ITEM_TEXT_ID         = 45
    DURABILITY           = 46
    MAX_DURABILITY       = 47


class UpdateFieldContainer(Enum):
    """ Hard limit: 0x5A """

    NUM_SLOTS = 48
    PAD       = 49
    SLOT_1    = 50


class UpdateFieldUnit(Enum):
    """ Hard limit: 0xB0 """

    CHARM                     = 6
    SUMMON                    = 8
    CHARMED_BY                = 10
    SUMMONED_BY               = 12
    CREATED_BY                = 14
    TARGET                    = 16
    PERSUADED                 = 18
    CHANNEL_OBJECT            = 20

    HEALTH                    = 22
    POWER_1                   = 23
    POWER_2                   = 24
    POWER_3                   = 25
    POWER_4                   = 26
    POWER_5                   = 27

    MAX_HEALTH                = 28
    MAX_POWER_1               = 29
    MAX_POWER_2               = 30
    MAX_POWER_3               = 31
    MAX_POWER_4               = 32
    MAX_POWER_5               = 33

    LEVEL                     = 34
    FACTION_TEMPLATE          = 35
    BYTES_0                   = 36
    VIRTUAL_ITEM_SLOT_DISPLAY = 37
    VIRTUAL_ITEM_INFO         = 40
    FLAGS                     = 46

    AURA                      = 47
    AURA_FLAGS                = 95
    AURA_LEVELS               = 101
    AURA_APPLICATIONS         = 113
    AURA_STATE                = 125

    BASE_ATTACK_TIME          = 126
    OFFHAND_ATTACK_TIME       = 127
    RANGED_ATTACK_TIME        = 128

    BOUNDING_RADIUS           = 129
    COMBAT_REACH              = 130

    DISPLAY_ID                = 131
    NATIVE_DISPLAY_ID         = 132
    MOUNT_DISPLAY_ID          = 133

    MIN_DAMAGE                = 134
    MAX_DAMAGE                = 135
    MIN_OFFHAND_DAMAGE        = 136
    MAX_OFFHAND_DAMAGE        = 137

    BYTES_1                   = 138

    PET_NUMBER                = 139
    PET_NAME_TIMESTAMP        = 140
    PET_EXPERIENCE            = 141
    PET_NEXT_LEVEL_EXP        = 142

    DYNAMIC_FLAGS             = 143
    CHANNEL_SPELL             = 144
    MOD_CAST_SPEED            = 145
    CREATED_BY_SPELL          = 146

    NPC_FLAGS                 = 147
    NPC_EMOTESTATE            = 148

    TRAINING_POINTS           = 149

    STAT_0                    = 150
    STAT_1                    = 151
    STAT_2                    = 152
    STAT_3                    = 153
    STAT_4                    = 154
    RESISTANCE_0              = 155
    RESISTANCE_1              = 156
    RESISTANCE_2              = 157
    RESISTANCE_3              = 158
    RESISTANCE_4              = 159
    RESISTANCE_5              = 160
    RESISTANCE_6              = 161

    BASE_MANA                 = 162
    BASE_HEALTH               = 163

    BYTES_2                   = 164

    ATTACK_POWER              = 165
    ATTACK_POWER_MODS         = 166
    ATTACK_POWER_MULT         = 167
    RANGED_ATTACK_POWER       = 168
    RANGED_ATTACK_POWER_MODS  = 169
    RANGED_ATTACK_POWER_MULT  = 170
    MIN_RANGED_DAMAGE         = 171
    MAX_RANGED_DAMAGE         = 172
    POWER_COST_MODIFIER       = 173
    POWER_COST_MULTIPLIER     = 180

    PADDING                   = 187


class UpdateFieldPlayer(Enum):
    """ Hard limit: 0x36C """

    DUEL_ARBITER                = 188
    FLAGS                       = 190

    GUILD_ID                    = 191
    GUILD_RANK                  = 192

    BYTES_1                     = 193  # originally "BYTES"
    BYTES_2                     = 194
    BYTES_3                     = 195

    DUEL_TEAM                   = 196
    GUILD_TIMESTAMP             = 197

    QUEST_LOG_1_1               = 198
    QUEST_LOG_1_2               = 199
    QUEST_LOG_2_1               = 201
    QUEST_LOG_2_2               = 202
    QUEST_LOG_3_1               = 204
    QUEST_LOG_3_2               = 205
    QUEST_LOG_4_1               = 207
    QUEST_LOG_4_2               = 208
    QUEST_LOG_5_1               = 210
    QUEST_LOG_5_2               = 211
    QUEST_LOG_6_1               = 213
    QUEST_LOG_6_2               = 214
    QUEST_LOG_7_1               = 216
    QUEST_LOG_7_2               = 217
    QUEST_LOG_8_1               = 219
    QUEST_LOG_8_2               = 220
    QUEST_LOG_9_1               = 222
    QUEST_LOG_9_2               = 223
    QUEST_LOG_10_1              = 225
    QUEST_LOG_10_2              = 226
    QUEST_LOG_11_1              = 228
    QUEST_LOG_11_2              = 229
    QUEST_LOG_12_1              = 231
    QUEST_LOG_12_2              = 232
    QUEST_LOG_13_1              = 234
    QUEST_LOG_13_2              = 235
    QUEST_LOG_14_1              = 237
    QUEST_LOG_14_2              = 238
    QUEST_LOG_15_1              = 240
    QUEST_LOG_15_2              = 241
    QUEST_LOG_16_1              = 243
    QUEST_LOG_16_2              = 244
    QUEST_LOG_17_1              = 246
    QUEST_LOG_17_2              = 247
    QUEST_LOG_18_1              = 249
    QUEST_LOG_18_2              = 250
    QUEST_LOG_19_1              = 252
    QUEST_LOG_19_2              = 253
    QUEST_LOG_20_1              = 255
    QUEST_LOG_20_2              = 256

    VISIBLE_ITEM_1_CREATOR      = 258
    VISIBLE_ITEM_1_ID           = 260
    VISIBLE_ITEM_1_PROPERTIES   = 268
    VISIBLE_ITEM_1_PAD          = 269
    VISIBLE_ITEM_2_CREATOR      = 270
    VISIBLE_ITEM_2_ID           = 272
    VISIBLE_ITEM_2_PROPERTIES   = 280
    VISIBLE_ITEM_2_PAD          = 281
    VISIBLE_ITEM_3_CREATOR      = 282
    VISIBLE_ITEM_3_ID           = 284
    VISIBLE_ITEM_3_PROPERTIES   = 292
    VISIBLE_ITEM_3_PAD          = 293
    VISIBLE_ITEM_4_CREATOR      = 294
    VISIBLE_ITEM_4_ID           = 296
    VISIBLE_ITEM_4_PROPERTIES   = 304
    VISIBLE_ITEM_4_PAD          = 305
    VISIBLE_ITEM_5_CREATOR      = 306
    VISIBLE_ITEM_5_ID           = 308
    VISIBLE_ITEM_5_PROPERTIES   = 316
    VISIBLE_ITEM_5_PAD          = 317
    VISIBLE_ITEM_6_CREATOR      = 318
    VISIBLE_ITEM_6_ID           = 320
    VISIBLE_ITEM_6_PROPERTIES   = 328
    VISIBLE_ITEM_6_PAD          = 329
    VISIBLE_ITEM_7_CREATOR      = 330
    VISIBLE_ITEM_7_ID           = 332
    VISIBLE_ITEM_7_PROPERTIES   = 340
    VISIBLE_ITEM_7_PAD          = 341
    VISIBLE_ITEM_8_CREATOR      = 342
    VISIBLE_ITEM_8_ID           = 344
    VISIBLE_ITEM_8_PROPERTIES   = 352
    VISIBLE_ITEM_8_PAD          = 353
    VISIBLE_ITEM_9_CREATOR      = 354
    VISIBLE_ITEM_9_ID           = 356
    VISIBLE_ITEM_9_PROPERTIES   = 364
    VISIBLE_ITEM_9_PAD          = 365
    VISIBLE_ITEM_10_CREATOR     = 366
    VISIBLE_ITEM_10_ID          = 368
    VISIBLE_ITEM_10_PROPERTIES  = 376
    VISIBLE_ITEM_10_PAD         = 377
    VISIBLE_ITEM_11_CREATOR     = 378
    VISIBLE_ITEM_11_ID          = 380
    VISIBLE_ITEM_11_PROPERTIES  = 388
    VISIBLE_ITEM_11_PAD         = 389
    VISIBLE_ITEM_12_CREATOR     = 390
    VISIBLE_ITEM_12_ID          = 392
    VISIBLE_ITEM_12_PROPERTIES  = 400
    VISIBLE_ITEM_12_PAD         = 401
    VISIBLE_ITEM_13_CREATOR     = 402
    VISIBLE_ITEM_13_ID          = 404
    VISIBLE_ITEM_13_PROPERTIES  = 412
    VISIBLE_ITEM_13_PAD         = 413
    VISIBLE_ITEM_14_CREATOR     = 414
    VISIBLE_ITEM_14_ID          = 416
    VISIBLE_ITEM_14_PROPERTIES  = 424
    VISIBLE_ITEM_14_PAD         = 425
    VISIBLE_ITEM_15_CREATOR     = 426
    VISIBLE_ITEM_15_ID          = 428
    VISIBLE_ITEM_15_PROPERTIES  = 436
    VISIBLE_ITEM_15_PAD         = 437
    VISIBLE_ITEM_16_CREATOR     = 438
    VISIBLE_ITEM_16_ID          = 440
    VISIBLE_ITEM_16_PROPERTIES  = 448
    VISIBLE_ITEM_16_PAD         = 449
    VISIBLE_ITEM_17_CREATOR     = 450
    VISIBLE_ITEM_17_ID          = 452
    VISIBLE_ITEM_17_PROPERTIES  = 460
    VISIBLE_ITEM_17_PAD         = 461
    VISIBLE_ITEM_18_CREATOR     = 462
    VISIBLE_ITEM_18_ID          = 464
    VISIBLE_ITEM_18_PROPERTIES  = 472
    VISIBLE_ITEM_18_PAD         = 473
    VISIBLE_ITEM_19_CREATOR     = 474
    VISIBLE_ITEM_19_ID          = 476
    VISIBLE_ITEM_19_PROPERTIES  = 484
    VISIBLE_ITEM_19_PAD         = 485

    INV_SLOT_HEAD               = 486

    PACK_SLOT_1                 = 532

    BANK_SLOT_1                 = 564

    BANK_BAG_SLOT_1             = 612

    VENDOR_BUY_BACK_SLOT_1      = 624

    KEYRING_SLOT_1              = 648

    FAR_SIGHT                   = 712
    COMBO_TARGET                = 714

    EXP                         = 716
    NEXT_LEVEL_XP               = 717

    SKILL_INFO_1_1              = 718

    CHARACTER_POINTS_1          = 1102
    CHARACTER_POINTS_2          = 1103

    TRACK_CREATURES             = 1104
    TRACK_RESOURCES             = 1105

    BLOCK_PERCENTAGE            = 1106
    DODGE_PERCENTAGE            = 1107
    PARRY_PERCENTAGE            = 1108
    CRIT_PERCENTAGE             = 1109
    RANGED_CRIT_PERCENTAGE      = 1110

    EXPLORED_ZONES_1            = 1111
    EXPLORED_ZONES_2            = 1112
    EXPLORED_ZONES_3            = 1113
    EXPLORED_ZONES_4            = 1114
    EXPLORED_ZONES_5            = 1115
    EXPLORED_ZONES_6            = 1116
    EXPLORED_ZONES_7            = 1117
    EXPLORED_ZONES_8            = 1118
    EXPLORED_ZONES_9            = 1119
    EXPLORED_ZONES_10           = 1120
    EXPLORED_ZONES_11           = 1121
    EXPLORED_ZONES_12           = 1122
    EXPLORED_ZONES_13           = 1123
    EXPLORED_ZONES_14           = 1124
    EXPLORED_ZONES_15           = 1125
    EXPLORED_ZONES_16           = 1126
    EXPLORED_ZONES_17           = 1127
    EXPLORED_ZONES_18           = 1128
    EXPLORED_ZONES_19           = 1129
    EXPLORED_ZONES_20           = 1130
    EXPLORED_ZONES_21           = 1131
    EXPLORED_ZONES_22           = 1132
    EXPLORED_ZONES_23           = 1133
    EXPLORED_ZONES_24           = 1134
    EXPLORED_ZONES_25           = 1135
    EXPLORED_ZONES_26           = 1136
    EXPLORED_ZONES_27           = 1137
    EXPLORED_ZONES_28           = 1138
    EXPLORED_ZONES_29           = 1139
    EXPLORED_ZONES_30           = 1140
    EXPLORED_ZONES_31           = 1141
    EXPLORED_ZONES_32           = 1142
    EXPLORED_ZONES_33           = 1143
    EXPLORED_ZONES_34           = 1144
    EXPLORED_ZONES_35           = 1145
    EXPLORED_ZONES_36           = 1146
    EXPLORED_ZONES_37           = 1147
    EXPLORED_ZONES_38           = 1148
    EXPLORED_ZONES_39           = 1149
    EXPLORED_ZONES_40           = 1150
    EXPLORED_ZONES_41           = 1151
    EXPLORED_ZONES_42           = 1152
    EXPLORED_ZONES_43           = 1153
    EXPLORED_ZONES_44           = 1154
    EXPLORED_ZONES_45           = 1155
    EXPLORED_ZONES_46           = 1156
    EXPLORED_ZONES_47           = 1157
    EXPLORED_ZONES_48           = 1158
    EXPLORED_ZONES_49           = 1159
    EXPLORED_ZONES_50           = 1160
    EXPLORED_ZONES_51           = 1161
    EXPLORED_ZONES_52           = 1162
    EXPLORED_ZONES_53           = 1163
    EXPLORED_ZONES_54           = 1164
    EXPLORED_ZONES_55           = 1165
    EXPLORED_ZONES_56           = 1166
    EXPLORED_ZONES_57           = 1167
    EXPLORED_ZONES_58           = 1168
    EXPLORED_ZONES_59           = 1169
    EXPLORED_ZONES_60           = 1170
    EXPLORED_ZONES_61           = 1171
    EXPLORED_ZONES_62           = 1172
    EXPLORED_ZONES_63           = 1173
    EXPLORED_ZONES_64           = 1174

    REST_STATE_EXPERIENCE       = 1175
    COINAGE                     = 1176

    POS_STAT_0                  = 1177
    POS_STAT_1                  = 1178
    POS_STAT_2                  = 1179
    POS_STAT_3                  = 1180
    POS_STAT_4                  = 1181
    NEG_STAT_0                  = 1182
    NEG_STAT_1                  = 1183
    NEG_STAT_2                  = 1184
    NEG_STAT_3                  = 1185
    NEG_STAT_4                  = 1186

    RESISTANCE_BUFF_MOD_POS     = 1187
    RESISTANCE_BUFF_MOD_NEG     = 1194

    MOD_DAMAGE_DONE_POS         = 1201
    MOD_DAMAGE_DONE_NEG         = 1208
    MOD_DAMAGE_DONE_PCT         = 1215

    BYTES_4                     = 1222  # originally "BYTES"

    AMMO_ID                     = 1223
    SELF_RES_SPELL              = 1224
    PVP_MEDALS                  = 1225

    BUYBACK_PRICE_1             = 1226
    BUYBACK_TIMESTAMP_1         = 1238

    SESSION_KILLS               = 1250
    YESTERDAY_KILLS             = 1251
    LAST_WEEK_KILLS             = 1252
    THIS_WEEK_KILLS             = 1253

    THIS_WEEK_CONTRIBUTION      = 1254
    LIFETIME_HONORABLE_KILLS    = 1255
    LIFETIME_DISHONORBALE_KILLS = 1256
    YESTERDAY_CONTRIBUTION      = 1257
    LAST_WEEK_CONTRIBUTION      = 1258
    LAST_WEEK_RANK              = 1259

    BYTES_5                     = 1260  # originally "BYTES2"

    WATCHED_FACTION_ID          = 1261
    COMBAT_RATING_1             = 1262


class UpdateFieldGameObject(Enum):
    """ Hard limit: 0x16 """

    CREATED_BY       = 6
    DISPLAY_ID       = 8
    FLAGS            = 9
    ROTATION         = 10
    STATE            = 14
    POS_X            = 15
    POS_Y            = 16
    POS_Z            = 17
    FACING           = 18
    DYN_FLAGS        = 19
    FACTION          = 20
    TYPE_ID          = 21
    LEVEL            = 22
    ART_KIT          = 23
    ANIM_PROGRESS    = 24
    PADDING          = 25


class UpdateFieldDynamicObject(Enum):
    """ Hard limit: 0x10 """

    CASTER   = 6
    BYTES    = 8
    SPELL_ID = 9
    RADIUS   = 10
    POS_X    = 11
    POS_Y    = 12
    POS_Z    = 13
    FACING   = 14
    PADDING  = 15


class UpdateFieldCorpse(Enum):
    """ Hard limit: 0x24 """

    OWNER         = 6
    FACING        = 8
    POS_X         = 9
    POS_Y         = 10
    POS_Z         = 11
    DISPLAY_ID    = 12
    ITEM          = 13
    BYTES_1       = 32
    BYTES_2       = 33
    GUILD         = 34
    FLAGS         = 35
    DYNAMIC_FLAGS = 36
    PADDING       = 37


class UpdateFieldsType(Enum):

    INT32 = 1  # 4
    INT64 = 2  # 8
    FLOAT = 3  # 4


UPDATE_FIELD_TYPE_MAP = {

    # --------------------
    # Object fields
    # --------------------

    UpdateFieldObject.GUID:    UpdateFieldsType.INT64,
    UpdateFieldObject.TYPE:    UpdateFieldsType.INT32,
    UpdateFieldObject.ENTRY:   UpdateFieldsType.INT32,
    UpdateFieldObject.SCALE_X: UpdateFieldsType.FLOAT,

    # --------------------
    # Unit fields
    # --------------------

    UpdateFieldUnit.SUMMON:                   UpdateFieldsType.INT64,
    UpdateFieldUnit.CHARMED_BY:               UpdateFieldsType.INT64,
    UpdateFieldUnit.SUMMONED_BY:              UpdateFieldsType.INT64,
    UpdateFieldUnit.CREATED_BY:               UpdateFieldsType.INT64,
    UpdateFieldUnit.TARGET:                   UpdateFieldsType.INT64,
    UpdateFieldUnit.PERSUADED:                UpdateFieldsType.INT64,
    UpdateFieldUnit.CHANNEL_OBJECT:           UpdateFieldsType.INT64,

    UpdateFieldUnit.HEALTH:                   UpdateFieldsType.INT32,
    UpdateFieldUnit.POWER_1:                  UpdateFieldsType.INT32,
    UpdateFieldUnit.POWER_2:                  UpdateFieldsType.INT32,
    UpdateFieldUnit.POWER_3:                  UpdateFieldsType.INT32,
    UpdateFieldUnit.POWER_4:                  UpdateFieldsType.INT32,
    UpdateFieldUnit.POWER_5:                  UpdateFieldsType.INT32,

    UpdateFieldUnit.MAX_HEALTH:               UpdateFieldsType.INT32,
    UpdateFieldUnit.MAX_POWER_1:              UpdateFieldsType.INT32,
    UpdateFieldUnit.MAX_POWER_2:              UpdateFieldsType.INT32,
    UpdateFieldUnit.MAX_POWER_3:              UpdateFieldsType.INT32,
    UpdateFieldUnit.MAX_POWER_4:              UpdateFieldsType.INT32,
    UpdateFieldUnit.MAX_POWER_5:              UpdateFieldsType.INT32,

    UpdateFieldUnit.LEVEL:                    UpdateFieldsType.INT32,
    UpdateFieldUnit.FACTION_TEMPLATE:         UpdateFieldsType.INT32,
    UpdateFieldUnit.BYTES_0:                  UpdateFieldsType.INT32,
    UpdateFieldUnit.FLAGS:                    UpdateFieldsType.INT32,

    UpdateFieldUnit.BASE_ATTACK_TIME:         UpdateFieldsType.INT32,
    UpdateFieldUnit.OFFHAND_ATTACK_TIME:      UpdateFieldsType.INT32,

    UpdateFieldUnit.BOUNDING_RADIUS:          UpdateFieldsType.FLOAT,
    UpdateFieldUnit.COMBAT_REACH:             UpdateFieldsType.FLOAT,

    UpdateFieldUnit.DISPLAY_ID:               UpdateFieldsType.INT32,
    UpdateFieldUnit.NATIVE_DISPLAY_ID:        UpdateFieldsType.INT32,
    UpdateFieldUnit.MOUNT_DISPLAY_ID:         UpdateFieldsType.INT32,

    UpdateFieldUnit.MIN_DAMAGE:               UpdateFieldsType.FLOAT,
    UpdateFieldUnit.MAX_DAMAGE:               UpdateFieldsType.FLOAT,
    UpdateFieldUnit.MIN_OFFHAND_DAMAGE:       UpdateFieldsType.FLOAT,
    UpdateFieldUnit.MAX_OFFHAND_DAMAGE:       UpdateFieldsType.FLOAT,

    UpdateFieldUnit.BYTES_1:                  UpdateFieldsType.INT32,

    UpdateFieldUnit.MOD_CAST_SPEED:           UpdateFieldsType.FLOAT,

    UpdateFieldUnit.STAT_0:                   UpdateFieldsType.INT32,
    UpdateFieldUnit.STAT_1:                   UpdateFieldsType.INT32,
    UpdateFieldUnit.STAT_2:                   UpdateFieldsType.INT32,
    UpdateFieldUnit.STAT_3:                   UpdateFieldsType.INT32,
    UpdateFieldUnit.STAT_4:                   UpdateFieldsType.INT32,
    UpdateFieldUnit.RESISTANCE_0:             UpdateFieldsType.INT32,
    UpdateFieldUnit.RESISTANCE_1:             UpdateFieldsType.INT32,
    UpdateFieldUnit.RESISTANCE_2:             UpdateFieldsType.INT32,
    UpdateFieldUnit.RESISTANCE_3:             UpdateFieldsType.INT32,
    UpdateFieldUnit.RESISTANCE_4:             UpdateFieldsType.INT32,
    UpdateFieldUnit.RESISTANCE_5:             UpdateFieldsType.INT32,
    UpdateFieldUnit.RESISTANCE_6:             UpdateFieldsType.INT32,

    UpdateFieldUnit.BASE_MANA:                UpdateFieldsType.INT32,
    UpdateFieldUnit.BASE_HEALTH:              UpdateFieldsType.INT32,

    UpdateFieldUnit.BYTES_2:                  UpdateFieldsType.INT32,

    UpdateFieldUnit.ATTACK_POWER:             UpdateFieldsType.INT32,
    UpdateFieldUnit.ATTACK_POWER_MODS:        UpdateFieldsType.INT32,
    UpdateFieldUnit.RANGED_ATTACK_POWER:      UpdateFieldsType.INT32,
    UpdateFieldUnit.RANGED_ATTACK_POWER_MODS: UpdateFieldsType.INT32,
    UpdateFieldUnit.MIN_RANGED_DAMAGE:        UpdateFieldsType.FLOAT,
    UpdateFieldUnit.MAX_RANGED_DAMAGE:        UpdateFieldsType.FLOAT,

    # --------------------
    # Player fields
    # --------------------

    UpdateFieldPlayer.FLAGS:                  UpdateFieldsType.INT32,

    UpdateFieldPlayer.BYTES_1:                UpdateFieldsType.INT32,  # skin 1
    UpdateFieldPlayer.BYTES_2:                UpdateFieldsType.INT32,  # skin 2
    UpdateFieldPlayer.BYTES_3:                UpdateFieldsType.INT32,  # gender

    UpdateFieldPlayer.VISIBLE_ITEM_1_ID:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.VISIBLE_ITEM_2_ID:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.VISIBLE_ITEM_3_ID:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.VISIBLE_ITEM_4_ID:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.VISIBLE_ITEM_5_ID:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.VISIBLE_ITEM_6_ID:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.VISIBLE_ITEM_7_ID:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.VISIBLE_ITEM_8_ID:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.VISIBLE_ITEM_9_ID:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.VISIBLE_ITEM_10_ID:     UpdateFieldsType.INT32,
    UpdateFieldPlayer.VISIBLE_ITEM_11_ID:     UpdateFieldsType.INT32,
    UpdateFieldPlayer.VISIBLE_ITEM_12_ID:     UpdateFieldsType.INT32,
    UpdateFieldPlayer.VISIBLE_ITEM_13_ID:     UpdateFieldsType.INT32,
    UpdateFieldPlayer.VISIBLE_ITEM_14_ID:     UpdateFieldsType.INT32,
    UpdateFieldPlayer.VISIBLE_ITEM_15_ID:     UpdateFieldsType.INT32,
    UpdateFieldPlayer.VISIBLE_ITEM_16_ID:     UpdateFieldsType.INT32,
    UpdateFieldPlayer.VISIBLE_ITEM_17_ID:     UpdateFieldsType.INT32,
    UpdateFieldPlayer.VISIBLE_ITEM_18_ID:     UpdateFieldsType.INT32,
    UpdateFieldPlayer.VISIBLE_ITEM_19_ID:     UpdateFieldsType.INT32,

    UpdateFieldPlayer.EXP:                    UpdateFieldsType.INT32,
    UpdateFieldPlayer.NEXT_LEVEL_XP:          UpdateFieldsType.INT32,

    UpdateFieldPlayer.CHARACTER_POINTS_1:     UpdateFieldsType.INT32,
    UpdateFieldPlayer.CHARACTER_POINTS_2:     UpdateFieldsType.INT32,

    UpdateFieldPlayer.BLOCK_PERCENTAGE:       UpdateFieldsType.FLOAT,
    UpdateFieldPlayer.DODGE_PERCENTAGE:       UpdateFieldsType.FLOAT,
    UpdateFieldPlayer.PARRY_PERCENTAGE:       UpdateFieldsType.FLOAT,
    UpdateFieldPlayer.CRIT_PERCENTAGE:        UpdateFieldsType.FLOAT,
    UpdateFieldPlayer.RANGED_CRIT_PERCENTAGE: UpdateFieldsType.FLOAT,

    UpdateFieldPlayer.EXPLORED_ZONES_1:       UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_2:       UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_3:       UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_4:       UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_5:       UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_6:       UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_7:       UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_8:       UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_9:       UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_10:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_11:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_12:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_13:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_14:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_15:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_16:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_17:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_18:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_19:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_20:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_21:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_22:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_23:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_24:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_25:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_26:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_27:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_28:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_29:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_30:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_31:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_32:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_33:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_34:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_35:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_36:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_37:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_38:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_39:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_40:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_41:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_42:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_43:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_44:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_45:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_46:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_47:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_48:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_49:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_50:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_51:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_52:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_53:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_54:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_55:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_56:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_57:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_58:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_59:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_60:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_61:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_62:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_63:      UpdateFieldsType.INT32,
    UpdateFieldPlayer.EXPLORED_ZONES_64:      UpdateFieldsType.INT32,

}


class ObjectUpdate(object):

    FIELD_BIN_MAP = {
        UpdateFieldsType.INT32: Struct("<I"),
        UpdateFieldsType.INT64: Struct("<Q"),
        UpdateFieldsType.FLOAT: Struct("<f")
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
        import binascii
        print(str(field) + " - " + binascii.hexlify(update_block).decode("ascii"))
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
        # Is that in this order? Do it with a reversed index if it doesn't work

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
        position = self.conn.character.position
        race = self.conn.character.race
        class_id = self.conn.character.class_id
        gender = self.conn.character.gender


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
        update.add(UpdateFieldUnit.NATIVE_DISPLAY_ID, 0)
        update.add(UpdateFieldUnit.MOUNT_DISPLAY_ID, 0)

        update.add(UpdateFieldUnit.MIN_DAMAGE, 0)
        update.add(UpdateFieldUnit.MAX_DAMAGE, 0)
        update.add(UpdateFieldUnit.MIN_OFFHAND_DAMAGE, 0)
        update.add(UpdateFieldUnit.MAX_OFFHAND_DAMAGE, 0)

        update.add(UpdateFieldUnit.BYTES_1, 0)  # stand state and stuff

        update.add(UpdateFieldUnit.MOD_CAST_SPEED, 1.0)

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
        update.add(UpdateFieldUnit.BASE_HEALTH, 1)

        update.add(UpdateFieldUnit.BYTES_2, 0)  # weapons sheathed and stuff

        update.add(UpdateFieldUnit.ATTACK_POWER, 0)
        update.add(UpdateFieldUnit.ATTACK_POWER_MODS, 0)
        update.add(UpdateFieldUnit.RANGED_ATTACK_POWER, 0)
        update.add(UpdateFieldUnit.RANGED_ATTACK_POWER_MODS, 0)

        update.add(UpdateFieldUnit.MIN_RANGED_DAMAGE, 0)
        update.add(UpdateFieldUnit.MAX_RANGED_DAMAGE, 0)




        # update mask block count, hard limit at 1C
        num_mask_blocks = len(update.mask_blocks)
        if num_mask_blocks >= 0x1C:
            LOG.critical("Too much update mask blocks, you fucked up something")
            raise Exception()
        data += int.to_bytes(num_mask_blocks, 1, "little")

        data += update.to_bytes()

        packet = WorldPacket(data)
        packet.opcode = OpCode.SMSG_UPDATE_OBJECT
        return packet
