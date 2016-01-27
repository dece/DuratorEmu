""" Some spell data extracted from the DBCs. """

from enum import Enum


class SpellId(Enum):
    """ Build 4125 spells IDs. Highest ID is 21184 ("Rogue Passive (DND)"). """

    DODGE                = 81
    ONE_HANDED_MACES     = 198
    UNARMED              = 203
    DEFENSE              = 204
    SPELLDEFENSE_DND     = 522
    SMITE                = 585
    LANGUAGE_ORCISH      = 669
    LESSER_HEAL          = 2050
    GENERIC_2382         = 2382
    HONORLESS_TARGET     = 2479
    DETECT               = 3050
    OPENING_3365         = 3365
    WANDS                = 5009
    SHOOT                = 5019
    UNDERWATER_BREATHING = 5227
    CLOSING_6233         = 6233
    CLOSING_6246         = 6246
    OPENING_6247         = 6247
    OPENING_6477         = 6477
    OPENING_6478         = 6478
    ATTACK               = 6603
    DUEL                 = 7266
    GROVEL               = 7267
    STUCK                = 7355
    WILL_OF_THE_FORSAKEN = 7744
    ATTACKING            = 8386
    CLOTH                = 9078
    GENERIC_9125         = 9125
    LANGUAGE_GUTTERSPEAK = 17737
    CANNIBALIZE          = 20577


# 0: Category
SPELL_VALUES = {
    SpellId.DODGE:                (   0, ),
    SpellId.ONE_HANDED_MACES:     (   0, ),
    SpellId.UNARMED:              (   0, ),
    SpellId.DEFENSE:              (   0, ),
    SpellId.SPELLDEFENSE_DND:     (   0, ),
    SpellId.SMITE:                (   0, ),
    SpellId.LANGUAGE_ORCISH:      (   0, ),
    SpellId.LESSER_HEAL:          (   0, ),
    SpellId.GENERIC_2382:         (   0, ),
    SpellId.HONORLESS_TARGET:     (   0, ),
    SpellId.DETECT:               (   0, ),
    SpellId.OPENING_3365:         (   0, ),
    SpellId.WANDS:                (   0, ),
    SpellId.SHOOT:                ( 351, ),
    SpellId.UNDERWATER_BREATHING: (   0, ),
    SpellId.CLOSING_6233:         (   0, ),
    SpellId.CLOSING_6246:         (   0, ),
    SpellId.OPENING_6247:         (   0, ),
    SpellId.OPENING_6477:         (   0, ),
    SpellId.OPENING_6478:         (   0, ),
    SpellId.ATTACK:               (   0, ),
    SpellId.DUEL:                 (   0, ),
    SpellId.GROVEL:               (   0, ),
    SpellId.STUCK:                (   0, ),
    SpellId.WILL_OF_THE_FORSAKEN: (   0, ),
    SpellId.ATTACKING:            (   0, ),
    SpellId.CLOTH:                (   0, ),
    SpellId.GENERIC_9125:         (   0, ),
    SpellId.LANGUAGE_GUTTERSPEAK: (   0, ),
    SpellId.CANNIBALIZE:          (   0, )
}
