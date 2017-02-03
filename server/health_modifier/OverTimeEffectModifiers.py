# -*- coding:utf-8 -*-
import time
from server.components.StatusModifierQueueElement import StatusModifierQueueElement
from server.health_modifier.AbstractStatusModifier import AbstractStatusModifier
from server.health_modifier.HungerThirstModifier import HungerIncreaseModifier


class HungerOverTimeEffect(AbstractStatusModifier):

    TYPE_ID = 101

    def __init__(self):
        AbstractStatusModifier.__init__(self, "HungerOverTimeEffect", HungerOverTimeEffect.TYPE_ID, visible=False)

    def ongoing_effect(self, player, status_modifier_component):
        if not status_modifier_component.has_status_type_in_queue(HungerOverTimeEffect.TYPE_ID):
            status_modifier_component.add_status_modifier_to_queue(StatusModifierQueueElement(
                HungerOverTimeEffect(), time.time() + 10
            ))

    def queue_time_is_up(self, player, status_modifier_component):
            status_modifier_component.add_status_modifier_to_queue(StatusModifierQueueElement(
                HungerIncreaseModifier(), 0
            ))