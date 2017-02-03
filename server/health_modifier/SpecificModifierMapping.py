# -*- coding:utf-8 -*-
from server.health_modifier.DamageFromEnemiesModifier import ShockedDamageModifier, SimpleDamageModifier
from server.health_modifier.HungerThirstModifier import HungerIncreaseModifier, HungerCompensationModifier, \
    ThirstIncreaseModifier, ThirstCompensationModifier
from server.health_modifier.OverTimeEffectModifiers import HungerOverTimeEffect
from server.health_modifier.SpecifiedModifiers import PoisonedModifier, VomitModifier, \
    PoisonReductionProbabilityEffect, AtmosphericPoison


class SpecificModifierMapping():

    mapping = {
        e.get_type(): e for e in [
            PoisonedModifier(),
            VomitModifier(),
            PoisonReductionProbabilityEffect(),
            AtmosphericPoison(),
            HungerIncreaseModifier(),
            HungerCompensationModifier(),
            ThirstIncreaseModifier(),
            ThirstCompensationModifier(),
            HungerOverTimeEffect(),
            ShockedDamageModifier(),
            SimpleDamageModifier()
        ]
    }

    @staticmethod
    def get_specific_modifier_by_type(type_id):
        return SpecificModifierMapping.mapping[type_id]