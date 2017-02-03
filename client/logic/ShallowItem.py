# -*- coding:utf-8 -*-
class ShallowItem():

    def __init__(self, game_object_id, item_uid, name, item_shape, item_tid, item_uses, item_start_position):
        self.container_game_object_id = game_object_id
        self.item_uid = item_uid
        self.name = name
        self.item_shape = item_shape
        self.item_tid = item_tid
        self.item_uses = item_uses
        self.item_start_position = item_start_position
        self.marked_deleting = False

    def mark_deleted(self):
        self.marked_deleting = True

    def is_marked_for_deletion(self):
        return self.marked_deleting

    def get_name(self):
        return self.name

    def get_uid(self):
        return self.item_uid

    def get_tid(self):
        return self.item_tid

    def get_shape(self):
        return self.item_shape

    def get_start_position(self):
        return self.item_start_position

    def set_start_position(self, pos):
        self.item_start_position = pos

    def get_num_uses(self):
        return self.item_uses

    def set_item_uses(self, new_uses):
        self.item_uses = new_uses