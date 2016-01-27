""" Default values for characters, races and classes.

Actually, I'm only going to support undead rogues for now. These values are
mostly taken from the WoWCore vanilla sandbox, so they may or may not be right,
but they're good enough for me. Skill values are current level and current stat
level (whatever that means).
"""

from durator.world.game.character.constants import CharacterRace, CharacterClass
from durator.world.game.object.type.unit import UnitPower
from durator.world.game.skill.constants import SkillId


# ------------------------------------------------------------------------------
# Defaults shared by all characters
# ------------------------------------------------------------------------------


NEW_CHAR_DEFAULTS = {
    "speed_walk":    2.5,
    "speed_run":     7.0,
    "speed_run_bw":  4.5,
    "speed_swim":    4.7222223,
    "speed_swim_bw": 2.5,
    "speed_turn":    3.141593,

    "level":        1,
    "unit_flags":   0,
    "unit_bytes_1": 0,

    "resistances": 0,  # don't we know these?

    "unit_bytes_2": 0,

    "player_flags": 0,

    "rest_info": 1,

    "exp":                0,
    "next_level_exp":     2500,
    "character_points_1": 0,
    "prof_left":          2,  # character_points_2

    "block_percentage": 4.0,
    "dodge_percentage": 4.0,
    "parry_percentage": 4.0,
    "crit_percentage":  4.0,

    "rest_state_exp": 200,
    "coinage":        0
}


# ------------------------------------------------------------------------------
# Defaults of each race
# ------------------------------------------------------------------------------


HUMAN_DEFAULTS = {
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

UNDEAD_DEFAULTS = {
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
# Defaults of each class (for each race)
# ------------------------------------------------------------------------------


UNDEAD_ROGUE_DEFAULTS = {
    "power_type":          UnitPower.ENERGY.value,

    "max_health":          65,
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

    "mod_cast_speed": 1,

    "stat_strength":  20,
    "stat_agility":   21,
    "stat_stamina":   22,
    "stat_intellect": 18,
    "stat_spirit":    25,

    "attack_power":     23,
    "base_mana":        0,
    "attack_power_mod": 0,

    "ap_ranged":         12,
    "ap_ranged_mod":     0,
    "min_ranged_damage": 5.54,
    "max_ranged_damage": 9.54,

    "skills": {
        SkillId.COMBAT:                (   5, 0 ),
        SkillId.SUBTLETY:              (   0, 0 ),
        SkillId.POISONS:               (   0, 0 ),
        SkillId.SWORDS:                (   0, 0 ),
        SkillId.BOWS:                  (   0, 0 ),
        SkillId.MACES:                 (   0, 0 ),
        SkillId.GUNS:                  (   0, 0 ),
        SkillId.DEFENSE:               (   1, 0 ),
        SkillId.LANGUAGE_ORCISH:       ( 300, 0 ),
        SkillId.LANGUAGE_DWARVEN:      (   0, 0 ),
        SkillId.LANGUAGE_DARNASSIAN:   (   0, 0 ),
        SkillId.LANGUAGE_TAURAHE:      (   0, 0 ),
        SkillId.DUAL_WIELD:            (   0, 0 ),
        SkillId.FIRST_AID:             (   0, 0 ),
        SkillId.LANGUAGE_THALASSIAN:   (   0, 0 ),
        SkillId.LANGUAGE_DRACONIC:     (   0, 0 ),
        SkillId.LANGUAGE_DEMON_TONGUE: (   0, 0 ),
        SkillId.LANGUAGE_TITAN:        (   0, 0 ),
        SkillId.LANGUAGE_OLD_TONGUE:   (   0, 0 ),
        SkillId.SURVIVAL:              (   0, 0 ),
        SkillId.HORSE_RIDING:          (   0, 0 ),
        SkillId.WOLF_RIDING:           (   0, 0 ),
        SkillId.TIGER_RIDING:          (   0, 0 ),
        SkillId.RAM_RIDING:            (   0, 0 ),
        SkillId.UNARMED:               (   1, 0 ),
        SkillId.BLACKSMITHING:         (   0, 0 ),
        SkillId.LEATHERWORKING:        (   0, 0 ),
        SkillId.ALCHEMY:               (   0, 0 ),
        SkillId.DAGGERS:               (   1, 0 ),
        SkillId.THROWN:                (   1, 0 ),
        SkillId.HERBALISM:             (   0, 0 ),
        SkillId.GENERIC_DND:           (   5, 0 ),
        SkillId.COOKING:               (   0, 0 ),
        SkillId.MINING:                (   0, 0 ),
        SkillId.TAILORING:             (   0, 0 ),
        SkillId.ENGINEERING:           (   0, 0 ),
        SkillId.RACIAL_UNDEAD:         (   5, 0 ),
        SkillId.CROSSBOWS:             (   0, 0 ),
        SkillId.ASSASSINATION:         (   5, 0 ),
        SkillId.LANGUAGE_GNOMISH:      (   0, 0 ),
        SkillId.LANGUAGE_TROLL:        (   0, 0 ),
        SkillId.ENCHANTING:            (   0, 0 ),
        SkillId.FISHING:               (   0, 0 ),
        SkillId.SKINNING:              (   0, 0 ),
        SkillId.LEATHER:               (   1, 0 ),
        SkillId.CLOTH:                 (   1, 0 ),
        SkillId.FIST_WEAPONS:          (   0, 0 ),
        SkillId.RAPTOR_RIDING:         (   0, 0 ),
        SkillId.UNDEAD_HORSEMANSHIP:   (   0, 0 ),
        SkillId.LOCKPICKING:           (   0, 0 ),
        SkillId.LANGUAGE_GUTTERSPEAK:  ( 300, 0 ),
        SkillId.KODO_RIDING:           (   0, 0 ),
        SkillId.JEWELCRAFTING:         (   0, 0 )
    },
}


# ------------------------------------------------------------------------------
# This map allows you to access the Defaults dicts easily with race and class
# ------------------------------------------------------------------------------


RACE_AND_CLASS_DEFAULTS = {
    (CharacterRace.UNDEAD, CharacterClass.ROGUE):
        { "race": UNDEAD_DEFAULTS, "class": UNDEAD_ROGUE_DEFAULTS }
}
