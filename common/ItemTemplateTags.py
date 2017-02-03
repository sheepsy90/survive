# -*- coding:utf-8 -*-
import collections


class ItemTemplateTags():


    WEAPON = "weapon"

    REPAIRED = "repaired"
    COMPONENT_AB = "component_ab"
    DAMAGED = "damaged"
    OPENED = "opened"
    CLOSED = "closed"

    # Consumable
    CONSUMABLE = "consumable"

    CONSUMES_AS_FOOD = "consumes_as_food"
    CONSUMES_AS_DRINK = "consumes_as_drink"


    AUTO_CONSUMES_ON_BAD_ATMOSPHERE = "consumes_on_bad_atmosphere"


    # Wearable Attributes
    WEARABLE = "wearable"
    HAND = "hand"
    MASK = "mask"

    # DoorRequirements
    SCIENCE_1 = "science_1"
    ADMINISTRATION_1 = "administration_1"
    TECHNICIAN_1 = "technician_1"
    SECURITY_1 = "security_1"

    SCIENCE_2 = "science_2"
    ADMINISTRATION_2 = "administration_2"
    TECHNICIAN_2 = "technician_2"
    SECURITY_2 = "security_2"

    SCIENCE_3 = "science_3"
    ADMINISTRATION_3 = "administration_3"
    TECHNICIAN_3 = "technician_3"
    SECURITY_3 = "security_3"

    @staticmethod
    def from_list(*args):
        """ USE THIS ONLY IN PERSISTENCE LAYER _ NOT AT RUNTIME !!!! """
        # Here are some constraints
        if ItemTemplateTags.WEARABLE in args:
            # Can has next to wearable only one position where it can be worn
            assert len({ItemTemplateTags.HAND, ItemTemplateTags.MASK}.intersection(args)) == 1
        return ",".join(args)


class ItemTemplateTagConsistencyChecker():

    @staticmethod
    def check():
        list = [value for key, value in vars(ItemTemplateTags).items() if not "from_list" in str(key) and not key.startswith("__")]
        counter = collections.Counter(list)
        for key, value in counter.items():
            assert value == 1, "ItemTemplateTag Value %s is used multiple times!" % key

    @staticmethod
    def check_input_list(input):
        list = [value for key, value in vars(ItemTemplateTags).items() if not "from_list" in str(key) and not key.startswith("__")]
        for word in input:
            assert word in list, "ItemTemplateTag Value %s is defined in level but not in ItemTemplateTags!" % word
