# -*- coding:utf-8 -*-
from common.constants.ScriptingConstants import ScriptingConstants
from common.named_tuples import IDSystemStats
from server.scripting.usable.AbstractUsableScript import AbstractUsableScript
from server.validators.IdSystemValidator import IdSystemValidator


class DigitalLockWithoutState(AbstractUsableScript):
    """ This is a simple usable script that can be attached to anything and
        just has a small cool down and checks for the correct ID requirements.
        Despite from that it doesn't remember a certain internal status and just
        sends of the event to the internal script attached to this when the
        requirements are met.
    """
    LABEL_KEY = "digital_lock_without_state"

    def initialize(self):
        self.usage_cool_down = 0.1

        self.intern_script_target = int(self.parameters["target"])
        assert self.intern_script_target > 0

        requirements = [int(u) for u in self.parameters["require"].split(",")]
        self.id_system_stats = IDSystemStats(security=requirements[0],
                                             technician=requirements[1],
                                             administration=requirements[2],
                                             science=requirements[3])

        self.internal_script = self.server_level.get_intern_script_manager()\
            .get_script(self.intern_script_target)

        self.internal_script.register(self.referenced_world_object)

    def use(self, player, item):
        """ This method is called from teh game whenever a player tries to use the world object
            When item and item_template is None - the player access this with his bare hands """

        if not self.check_cool_down_over():
            return ScriptingConstants.IN_COOL_DOWN

        if self.uses_bare_hands(item):
            return ScriptingConstants.ID_CARD_REQUIRED

        item_template = item.get_item_template()

        if not IdSystemValidator.is_requirement_met(item_template, self.id_system_stats):
            return ScriptingConstants.NOT_AUTHORIZED

        return self.internal_script.handle_event(player, self.referenced_world_object)