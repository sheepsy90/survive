# -*- coding:utf-8 -*-
import random
import time
from common.ItemTemplateTags import ItemTemplateTags
from server.components.StatusModifierQueueElement import StatusModifierQueueElement

from server.health_modifier.AbstractStatusModifier import AbstractStatusModifier
from server.health_modifier.HungerThirstModifier import ThirstIncreaseModifier


class PoisonedModifier(AbstractStatusModifier):

    TYPE_ID = 1

    def __init__(self):
        AbstractStatusModifier.__init__(self, "Poisioned", PoisonedModifier.TYPE_ID)

    def ongoing_effect(self, player, status_modifier_component):
        # First handle the case that AtmosphericPoison is not present then we reduce the poison again
        if not status_modifier_component.has_status_type_in_queue(PoisonReductionProbabilityEffect().get_type()) and \
                status_modifier_component.get_status_type_count(AtmosphericPoison().get_type()) == 0:
            status_modifier_component.add_status_modifier_to_queue(
                StatusModifierQueueElement(PoisonReductionProbabilityEffect(), time.time()+5))

        if status_modifier_component.get_status_type_count(self.get_type()) > 5 and \
            not status_modifier_component.has_status_type(VomitModifier().get_type()):
            status_modifier_component.add_status_modifier_to_queue(StatusModifierQueueElement(VomitModifier(), 0))

    def queue_time_is_up(self, player, status_modifier_component):
        # This is performed when the time is up and the queued status_modifier needs to be handled
        wearing_handler = player.get_character_wearing_handler()
        result = wearing_handler.get_mask_item_and_template()

        if result is not None:
            mask_item, item_template = result
            if mask_item is not None and item_template.has_tag(ItemTemplateTags.AUTO_CONSUMES_ON_BAD_ATMOSPHERE):
                if mask_item.decrease_usage_true_on_zero():
                    mask_item.mark_deleting()
                player.add_item_to_changed_set(mask_item)
                return

        # When there is no mask we need to increase the poison value
        if status_modifier_component.get_status_type_count(self.get_type()) < 9:
            status_modifier_component.increase_modifier(self.get_type(), 1)


class VomitModifier(AbstractStatusModifier):

    TYPE_ID = 2

    def __init__(self):
        AbstractStatusModifier.__init__(self, "Vomit", VomitModifier.TYPE_ID)

    def ongoing_effect(self, player, status_modifier_component):
        if not status_modifier_component.has_status_type_in_queue(ThirstIncreaseModifier.TYPE_ID):
            status_modifier_component.add_status_modifier_to_queue(StatusModifierQueueElement(
                ThirstIncreaseModifier(), time.time() + 5
            ))

    def queue_time_is_up(self, player, status_modifier_component):
        status_modifier_component.set_modifier(VomitModifier.TYPE_ID, 1)


class AtmosphericPoison(AbstractStatusModifier):

    TYPE_ID = 3

    def __init__(self):
        AbstractStatusModifier.__init__(self, "Poision", AtmosphericPoison.TYPE_ID)

    def ongoing_effect(self, player, status_modifier_component):
        if not status_modifier_component.has_status_type_in_queue(PoisonedModifier.TYPE_ID):
            status_modifier_component.add_status_modifier_to_queue(StatusModifierQueueElement(PoisonedModifier(),
                                                                                              time.time() + 5))


class PoisonReductionProbabilityEffect(AbstractStatusModifier):

    TYPE_ID = 201

    def __init__(self):
        AbstractStatusModifier.__init__(self, "PoisionReductionProbabilityEffect",
                                        PoisonReductionProbabilityEffect.TYPE_ID)

    def queue_time_is_up(self, player, health_system):
        # This Effect doesn't add itself to any permanent stats but it's going
        # to throw a dice whether to reduce the degree of poison
        if random.random() > 0.5:
            health_system.decrease_modifier(PoisonedModifier().get_type(), 1)


