# -*- coding:utf-8 -*-
from common.ItemTemplateTags import ItemTemplateTags
from common.constants.ScriptingConstants import ScriptingConstants
from server.scripting.usable.AbstractUsableScript import AbstractUsableScript


class RescueCapsuleScript(AbstractUsableScript):

    def initialize(self):
        self.usage_cool_down = 1

    def use(self, player, item):
        """ This method is called from teh game whenever a player tries to use the world object
            When item and item_template is None - the player access this with his bare hands """
        item_template = item.get_item_template()

        if not self.check_cool_down_over():
            return ScriptingConstants.IN_COOL_DOWN

        if self.referenced_world_object.has_tag(ItemTemplateTags.DAMAGED) and self.uses_bare_hands(item):
            # TODO Nothing happened but we need a feedback mechanism
            return ScriptingConstants.NOTHING_CHANGED

        elif self.referenced_world_object.has_tag(ItemTemplateTags.DAMAGED) \
                and not self.uses_bare_hands(item) and item_template.has_tag(ItemTemplateTags.COMPONENT_AB):
            self.referenced_world_object.remove_tag(ItemTemplateTags.DAMAGED)
            self.referenced_world_object.add_tag(ItemTemplateTags.REPAIRED)
            item.mark_deleting()
            player.add_item_to_changed_set(item)
            return ScriptingConstants.REPAIRED

        elif self.referenced_world_object.has_tag(ItemTemplateTags.REPAIRED) and self.uses_bare_hands(item):
            player.set_finished_tutorial()
            return ScriptingConstants.RESCUE_ACTIVATED

        return ScriptingConstants.NOTHING_CHANGED