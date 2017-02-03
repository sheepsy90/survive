# -*- coding:utf-8 -*-
from common.ItemTemplateTags import ItemTemplateTags

from common.constants.ScriptingConstants import ScriptingConstants
from common.named_tuples import IDSystemStats
from server.scripting.usable.AbstractUsableScript import AbstractUsableScript
from server.validators.IdSystemValidator import IdSystemValidator


class DigitalLockWithState(AbstractUsableScript):
    """ This is a simple usable script that can be attached to anything and
        has a cool down and checks for the correct ID requirements.

        Furthermore it switches internally the state each time it is used.
        So an attached internal script is able to determine its status.
    """
    LABEL_KEY = "digital_lock_with_state"

    def initialize(self):
        self.usage_cool_down = 1

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

        if self.referenced_world_object.has_tag(ItemTemplateTags.CLOSED):
            self.referenced_world_object.remove_tag(ItemTemplateTags.CLOSED)
            self.referenced_world_object.add_tag(ItemTemplateTags.OPENED)
            return self.internal_script.handle_event(player, self.referenced_world_object)
        elif self.referenced_world_object.has_tag(ItemTemplateTags.OPENED):
            self.referenced_world_object.remove_tag(ItemTemplateTags.OPENED)
            self.referenced_world_object.add_tag(ItemTemplateTags.CLOSED)
            return self.internal_script.handle_event(player, self.referenced_world_object)

        return ScriptingConstants.NOTHING_CHANGED





