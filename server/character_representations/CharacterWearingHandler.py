# -*- coding:utf-8 -*-
from common.ItemTemplateTags import ItemTemplateTags


def log_for_dev(original_function):
    def new_function(s, arg):
        print "Called", str(original_function).split(" ")[1], "with", arg
        return original_function(s, arg)
    return new_function


class TwoWayAssocDict():

    def __init__(self):
        self.a_to_b = {}
        self.b_to_a = {}

    def add_pair(self, first, second):
        if first not in self.a_to_b and second not in self.b_to_a:
            self.a_to_b[first] = second
            self.b_to_a[second] = first
            return True
        else:
            return False

    def get_by_key(self, key, first_arg=True):
        if first_arg:
            if key in self.a_to_b:
                return self.a_to_b[key]
        else:
            if key in self.b_to_a:
                return self.b_to_a[key]

    def delete_by(self,  key, first_arg=True):
        if first_arg:
            val = self.a_to_b[key]
            self.a_to_b.__delitem__(key)
            self.b_to_a.__delitem__(val)
        else:
            val = self.b_to_a[key]
            self.a_to_b.__delitem__(val)
            self.b_to_a.__delitem__(key)

    def update_by(self, key, value, first_arg=True):
        if first_arg:
            self.a_to_b[key] = value
            self.b_to_a[value] = key
        else:
            self.a_to_b[value] = key
            self.b_to_a[key] = value

class CharacterWearingHandler(object):
    """ This class handles the items the player currently wears """

    def __init__(self, item_template_service_client):
        self.item_template_service_client = item_template_service_client

        self.slot_tags = {ItemTemplateTags.MASK, ItemTemplateTags.HAND}

        self.slot_mapping = TwoWayAssocDict()

        for element in self.slot_tags:
            self.slot_mapping.add_pair(element, None)

        self.items_currently_worn = {}

    def is_item_worn(self, item_id):
        return item_id in self.items_currently_worn.keys()

    def try_wearing_item(self, item):
        item_id = item.get_id()
        type_id = item.get_type_id()
        item_template = self.item_template_service_client.get_item_template(type_id)
        item_tag_set = item_template.get_type_set()
        is_wearable = ItemTemplateTags.WEARABLE in item_tag_set
        already_worn = self.is_item_worn(item_id)

        if is_wearable and not already_worn:
            slot_set = item_tag_set.intersection(self.slot_tags)

            if len(slot_set) != 1:
                print "[ERROR] Wearable has not a slot definition", item_template
                return False

            slot = list(slot_set)[0]
            element = self.slot_mapping.get_by_key(slot)

            if element is None:
                self.slot_mapping.update_by(slot, item)
                self.items_currently_worn[item.get_id()] = [item, item_template]
                return True

        return False

    def get_wearing_type(self, item):
        return self.slot_mapping.get_by_key(item, first_arg=False)

    def get_mask_item_and_template(self):
        item = self.slot_mapping.get_by_key(ItemTemplateTags.MASK)
        if item is None:
            return None
        else:
            return self.items_currently_worn[item.get_id()]

    def get_worn_item_by_slot(self, slot):
        item = self.slot_mapping.get_by_key(slot)
        if item is not None:
            return self.items_currently_worn[item.get_id()]

    def unwear_item(self, item_id):
        if item_id in self.items_currently_worn.keys():
            item = self.items_currently_worn[item_id][0]
            slot_key = self.slot_mapping.get_by_key(item, first_arg=False)
            self.slot_mapping.update_by(slot_key, None)
            self.items_currently_worn.__delitem__(item_id)

    def get_worn_item_values(self):
        return self.items_currently_worn.values()

    def get_worn_items_ids_as_list(self):
        return self.items_currently_worn.keys()