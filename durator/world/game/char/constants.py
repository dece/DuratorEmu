""" Constants values for characters, races and classes. """

from enum import Enum


# ------------------------------------------------------------------------------
# Constants shared by all characters
# ------------------------------------------------------------------------------


class CharacterRace(Enum):

    HUMAN     = 1
    ORC       = 2
    DWARF     = 3
    NIGHT_ELF = 4
    UNDEAD    = 5
    TAUREN    = 6
    GNOME     = 7
    TROLL     = 8


class CharacterClass(Enum):

    NONE    = 0
    WARRIOR = 1
    PALADIN = 2
    HUNTER  = 3
    ROGUE   = 4
    PRIEST  = 5
    SHAMAN  = 7
    MAGE    = 8
    WARLOCK = 9
    DRUID   = 11


class CharacterGender(Enum):

    MALE   = 0
    FEMALE = 1


class UnitPower(Enum):

    MANA      = 0
    RAGE      = 1
    FOCUS     = 2
    ENERGY    = 3
    HAPPINESS = 4


class UnitStats(Enum):

    STRENGTH  = 0
    AGILITY   = 1
    STAMINA   = 2
    INTELLECT = 3
    SPIRIT    = 4


class CharacterEquipSlot(Enum):

    HEAD      = 0
    NECK      = 1
    SHOULDERS = 2
    BODY      = 3
    CHEST     = 4
    WAIST     = 5
    LEGS      = 6
    FEET      = 7
    WRISTS    = 8
    HANDS     = 9
    FINGER1   = 10
    FINGER2   = 11
    TRINKET1  = 12
    TRINKET2  = 13
    BACK      = 14
    MAINHAND  = 15
    OFFHAND   = 16
    RANGED    = 17
    TABARD    = 18
    BAG1      = 19
    BAG2      = 20
    BAG3      = 21
    BAG4      = 22


NEW_CHAR_CONSTS = {
    "speed_walk":    2.5,
    "speed_run":     7.0,
    "speed_run_bw":  4.5,
    "speed_swim":    4.7222223,
    "speed_swim_bw": 2.5,
    "speed_turn":    3.141593,

    "level":            1,
    "exp":              100,
    "next_level_exp":   2500,
    "professions_left": 2,
    "coinage":          1230000,
    "rest_info":        1,
    "rest_state_exp":   200
}


# ------------------------------------------------------------------------------
# Constants of each race
# ------------------------------------------------------------------------------


HUMAN_CONSTS = {
    "scale_x":           1.0,
    "start_map":         0,
    "start_zone":        12,
    "start_pos_x":       -8949.950195,
    "start_pos_y":       -132.492996,
    "start_pos_z":       83.531197,
    "start_orientation": 0.000000,
    "bounding_radius":   0.306000,
    "combat_reach":      1.500000,
    "model_male":        49,
    "model_female":      50,
    "faction_template":  CharacterRace.HUMAN.value
}

UNDEAD_CONSTS = {
    "scale_x":           1.0,
    "start_map":         0,
    "start_zone":        85,
    "start_pos_x":       1676.349976,
    "start_pos_y":       1677.449951,
    "start_pos_z":       121.669998,
    "start_orientation": 2.705260,
    "bounding_radius":   0.382999,
    "combat_reach":      1.500000,
    "model_male":        57,
    "model_female":      58,
    "faction_template":  CharacterRace.UNDEAD.value
}


# ------------------------------------------------------------------------------
# Constants of each class (for each race)
# ------------------------------------------------------------------------------


UNDEAD_ROGUE_CONSTS = {
    "max_health":          65,
    "power_type":          UnitPower.ENERGY.value,
    "max_power_mana":      0,
    "max_power_rage":      0,
    "max_power_focus":     0,
    "max_power_energy":    100,
    "max_power_happiness": 0,

    "attack_time_mainhand": 1600,
    "attack_time_offhand":  2000,
    "attack_time_ranged":   1800,

    "min_damage":         3.63,
    "max_damage":         4.63,
    "min_offhand_damage": 0.0,
    "max_offhand_damage": 0.0,
    "min_ranged_damage":  5.54,
    "max_ranged_damage":  9.54,

    "mod_cast_speed": 1,

    "stat_strength":  20,
    "stat_agility":   21,
    "stat_stamina":   22,
    "stat_intellect": 18,
    "stat_spirit":    25,

    "base_mana":   0,

    "attack_power":            23,
    "attack_power_mod":        0,
    "attack_power_ranged":     12,
    "attack_power_ranged_mod": 0,
}
