# -*- coding:utf-8 -*-
from common.ItemTemplateTags import ItemTemplateTags


class WearingManager(object):

    def __init__(self):
        self.wearing = {}

    def is_wearing(self, uid):
        return uid in self.wearing

    def get_wearing_slot(self, uid):
        return self.wearing.get(uid, None)

    def add_item_wearing(self, uid, slot):
        if uid not in self.wearing:
            self.wearing[uid] = slot

    def remove_item_wearing(self, uid):
        if uid in self.wearing:
            self.wearing.__delitem__(uid)

    def is_wearing_mask(self):
        return ItemTemplateTags.MASK in self.wearing.values()