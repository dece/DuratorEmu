from durator.world.game.object.object_fields import PlayerField
from durator.world.game.object.unit import Unit
from durator.world.game.skill.skill import Skill


NUM_TUTORIALS      = 64
NUM_SKILLS         = 128
NUM_SPELLS         = 100
NUM_ACTION_BUTTONS = 120
NUM_REPUTATIONS    = 128
NUM_VISIBLE_ITEMS  = 19


class Player(Unit):
    """ A Player is a Unit controlled by a human player. """

    def __init__(self):
        super().__init__()
        self.skills = []

    def import_skills(self, char_data):
        skills = ( Skill
                   .select()
                   .where(Skill.character == char_data)
                   .order_by(Skill.ident)
                   .limit(NUM_SKILLS) )
        for skill in skills:
            slot = len(self.skills)
            self.skills.append(skill)
            self._set_skill_fields(slot, skill)

    def _set_skill_fields(self, slot, skill):
        id_field         = PlayerField.SKILL_INFO_1_ID.value + slot*3
        level_field      = PlayerField.SKILL_INFO_1_LEVEL.value + slot*3
        stat_level_field = PlayerField.SKILL_INFO_1_STAT_LEVEL.value + slot*3

        self.set(id_field, skill.ident)

        level_value = skill.level | skill.max_level << 16
        self.set(level_field, level_value)

        stat_level_value = skill.stat_level | skill.stat_max_level << 16
        self.set(stat_level_field, stat_level_value)

    def export_skills(self):
        for skill in self.skills:
            skill.save()
