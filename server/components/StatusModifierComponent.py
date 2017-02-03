# -*- coding:utf-8 -*-
import time
from server.health_modifier.SpecificModifierMapping import SpecificModifierMapping


class ModifierComponent(object):
    """ This is the status modifier component which is bound to the
        player and handles his status effects like, hunger, thirst, medical needs, damage, euphoria, whatever
    """

    def __init__(self, player):
        # The player the component belongs to
        self.player = player

        # First of all we have a key-value structure of giving information what modifiers are
        # currently assigned to the player
        self.modifiers = {}

        # Secondly there is a queue of modifiers which are scheduled
        self.modifier_queue = []

    def set_modifier_queue(self, queue):
        """ Set the modifier queue to a given value for player loading """
        self.modifier_queue = queue

    def set_modifier(self, mod_type, amount):
        """ Set a modifier to a specific value - this is used on loading a player """
        self.modifiers[mod_type] = amount

    def update(self):
        """ This method handles the update for the StatusModifierComponent """

        # Step 1 - Look into all queue elements sorted by time and handle those who's time is up
        self.modifier_queue = sorted(self.modifier_queue, key=lambda e: e.time_stamp_to_activate)
        self.current_time = time.time()

        new_modifier_queue = [e for e in self.modifier_queue if e.time_stamp_to_activate >= self.current_time]
        queue_elements_need_handling = [e for e in self.modifier_queue if e.time_stamp_to_activate < self.current_time]

        self.modifier_queue = new_modifier_queue

        for queue_element in queue_elements_need_handling:
            queue_element.status_effect.queue_time_is_up(self.player, self)

        # Step 2 - Iterate over all ongoing status effects and execute their effects
        for element in self.modifiers:
            modifier = SpecificModifierMapping.get_specific_modifier_by_type(element)
            modifier.ongoing_effect(self.player, self)

    def get_status_type_count(self, mod_type_id):
        return self.modifiers.get(mod_type_id, 0)

    def has_status_type(self, mod_type_id):
        return self.get_status_type_count(mod_type_id) > 0

    def get_modifiers(self):
        return self.modifiers

    def increase_modifier(self, mod_type, amount):
        if mod_type not in self.modifiers:
            self.modifiers[mod_type] = amount
        else:
            self.modifiers[mod_type] += amount

    def decrease_modifier(self, mod_type, amount):
        if mod_type in self.modifiers:
            value = self.modifiers[mod_type]
            if value - amount <= 0:
                self.unset_modifier(mod_type)
            else:
                self.modifiers[mod_type] -= amount

    def unset_modifier(self, mod_type):
        if mod_type in self.modifiers:
            self.modifiers.__delitem__(mod_type)

    def has_status_type_in_queue(self, mod_type_id):
        return mod_type_id in [e.status_effect.get_type() for e in self.modifier_queue]

    def add_status_modifier_to_queue(self, status_modifier_queue_element):
        """ This element adds a new status effect to the status_modifier queue
            Before doing so it calls the added_to_queue method on the status_modifier
            Only when this returns true the queue element is added
        """

        if status_modifier_queue_element.status_effect.added_to_queue(self.player, self):
            # The method returns true which means that there is the need to put that element into the queue
            self.modifier_queue.append(status_modifier_queue_element)

