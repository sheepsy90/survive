# -*- coding:utf-8 -*-
import time
from common.ItemTemplateTags import ItemTemplateTags
from common.constants.ScriptingConstants import ScriptingConstants
from server.scripting.usable.DigitalLockWithState import DigitalLockWithState
from server.validators.IdSystemValidator import IdSystemValidator


class DigitalLockWithStateResetsAutomatically(DigitalLockWithState):
    """ This is a simple usable script that can be attached to anything and
        has a cool down and checks for the correct ID requirements.

        Furthermore it switches internally the state each time it is used.
        So an attached internal script is able to determine its status.

        It resets itself after a short period of time when used again,
        or when the check method is called (usually by an internal script).
    """

    LABEL_KEY = "digital_lock_with_state_resets_automatically"

    def initialize(self):
        DigitalLockWithState.initialize(self)

        self.last_time_opened = None

    def check(self):
        print "Checking Usable Components"
        if self.last_time_opened is not None and (time.time() - self.last_time_opened) > 3:
            print "Times up"
            self.referenced_world_object.remove_tag(ItemTemplateTags.OPENED)
            self.referenced_world_object.add_tag(ItemTemplateTags.CLOSED)
            self.last_time_opened = None
            return True

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

        # Check the internal state before evaluating the true new state
        self.check()

        if self.referenced_world_object.has_tag(ItemTemplateTags.CLOSED):
            self.last_time_opened = time.time()
            self.referenced_world_object.remove_tag(ItemTemplateTags.CLOSED)
            self.referenced_world_object.add_tag(ItemTemplateTags.OPENED)
            return self.internal_script.handle_event(player, self.referenced_world_object)
        elif self.referenced_world_object.has_tag(ItemTemplateTags.OPENED):
            self.last_time_opened = None
            self.referenced_world_object.remove_tag(ItemTemplateTags.OPENED)
            self.referenced_world_object.add_tag(ItemTemplateTags.CLOSED)
            return self.internal_script.handle_event(player, self.referenced_world_object)

        return ScriptingConstants.NOTHING_CHANGED
