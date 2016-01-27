from durator.db.database import db_connection
from durator.world.game.object.object_fields import PlayerField
from durator.world.game.object.unit import Unit
from durator.world.game.skill.constants import SkillIdent
from durator.world.game.skill.defaults import SKILL_MAX_LEVELS
from durator.world.game.skill.skill import Skill


class Player(Unit):
    """ A Player is a Unit controlled by a human player. """

    NUM_TUTORIALS      = 64
    NUM_SKILLS         = 128
    NUM_SPELLS         = 100
    NUM_ACTION_BUTTONS = 120
    NUM_REPUTATIONS    = 128
    NUM_VISIBLE_ITEMS  = 19

    def __init__(self):
        super().__init__()
        self.skills = []

    @db_connection
    def import_skills(self, char_data):
        """ Import skills in the local skills list and in the update fields. """
        skills = ( Skill
                   .select()
                   .where(Skill.character == char_data)
                   .order_by(Skill.ident)
                   .limit(self.NUM_SKILLS) )
        for skill in skills:
            slot = len(self.skills)
            self.skills.append(skill)
            self._set_skill_fields(slot, skill)

    def _set_skill_fields(self, slot, skill):
        """ Update the object's fields for that skill at this skill slot. """
        id_field         = PlayerField.SKILL_INFO_1_ID.value + slot*3
        level_field      = PlayerField.SKILL_INFO_1_LEVEL.value + slot*3
        stat_level_field = PlayerField.SKILL_INFO_1_STAT_LEVEL.value + slot*3

        self.set(id_field, skill.ident)

        level, stat_level = skill.level, skill.stat_level
        max_level, max_stat_level = SKILL_MAX_LEVELS[SkillIdent(skill.ident)]

        level_values = level | max_level << 16
        self.set(level_field, level_values)

        stat_level_values = stat_level | max_stat_level << 16
        self.set(stat_level_field, stat_level_values)

    @db_connection
    def export_skills(self):
        """ Save the local list of skills in the database. """
        for skill in self.skills:
            skill.save()
