# -*- coding:utf-8 -*-

class DescriptionManager(object):

    def __init__(self, client_socket_wrapper):
        self.client_socket_wrapper = client_socket_wrapper

        self.has_description_possibility = False
        self.item_type_id_to_note_at = None

    def has_available_description_possibility(self):
        return self.has_description_possibility

    def set_description_possibility(self, item_type_id):
        self.has_description_possibility = True
        self.item_type_id_to_note_at = item_type_id

    def finish_description(self, text):
        self.client_socket_wrapper.send_item_type_description(self.item_type_id_to_note_at, text)
        self.has_description_possibility = False
        self.item_type_id_to_note_at = None