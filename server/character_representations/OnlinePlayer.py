from Queue import Queue
import time
from common.ItemTemplateTags import ItemTemplateTags
from common.constants.ContainerConstants import ContainerConstants
from server.components.MovableComponent import MovableComponent
from server.components.PersistableComponent import PersistableComponent
from server.components.StatusModifierComponent import ModifierComponent
from server.world_objects.object_components.ContainerComponent import Container





class OnlinePlayer():

    def __init__(self, account_id, character_id, name, tutorial_state, connection, additional_information):
        self.account_id = account_id
        self.character_id = character_id
        self.name = name
        self.connection = connection
        self.tutorial_state = tutorial_state

        self.components = {}
        self.components["MovableComponent"] = MovableComponent(additional_information['pos'])
        self.components["CharacterModifierComponent"] = ModifierComponent(self)
        self.components["PersistableComponent"] = PersistableComponent()

        self.backpack_container = Container(refreshable=False, shape=(8, 8), container_type=ContainerConstants.CONTAINER_TYPE_BACKPACK)
        self.backpack_container.set_parent(self)
        self.backpack_container.prepare_content(empty=True)

        self.crafting_container = Container(refreshable=False, shape=(6, 6), container_type=ContainerConstants.CONTAINER_TYPE_CRAFTING)
        self.crafting_container.set_parent(self)
        self.crafting_container.prepare_content(empty=True)

        self.character_wearing_handler = None
        self.changed_during_iteration_item_list = []

        self.command_queue = Queue()
        self.disconnecting = False
        self.searching_process = None
        self.finished_tutorial = None

    def set_finished_tutorial(self):
        self.finished_tutorial = time.time()
        self.tutorial_state = 0

    def is_finished_tutorial(self):
        return self.finished_tutorial

    def is_player_still_tutorial(self):
        return self.tutorial_state

    # Service Getter Methods
    def get_moving_component(self):
        return self.components["MovableComponent"]

    def get_health_modifier_component(self):
        return self.components["CharacterModifierComponent"]

    def get_persistable_component(self):
        return self.components["PersistableComponent"]

    def get_inventory(self):
        return self.backpack_container

    def get_crafting_container(self):
        return self.crafting_container

    def get_character_wearing_handler(self):
        return self.character_wearing_handler

    def set_character_wearing_handler(self, value):
        self.character_wearing_handler = value

    def add_item_to_changed_set(self, item):
        self.changed_during_iteration_item_list.append(item)

    def get_items_changed_during_iteration(self):
        return self.changed_during_iteration_item_list

    def clear_items_changed_during_iteration(self):
        self.changed_during_iteration_item_list = []

    # Native Methods
    def get_account_id(self):
        return self.account_id

    def get_character_id(self):
        return self.character_id

    def get_name(self):
        return self.name

    def get_id(self):
        return self.character_id

    def get_object_id(self):
        return self.character_id

    def get_connection(self):
        return self.connection

    def add_command(self, comm, data):
        self.command_queue.put((comm, data))

    def get_open_commands(self):
        return self.command_queue.get()

    def has_open_command(self):
        return not self.command_queue.empty()

    def mark_disconnecting(self):
        self.disconnecting = True

    def is_disconnecting(self):
        return self.disconnecting

    def get_item_and_item_template_player_has_in_hand(self):
    # Now we get the item that the player holds in his hand
        char_wearing_handler = self.get_character_wearing_handler()
        result = char_wearing_handler.get_worn_item_by_slot(ItemTemplateTags.HAND)
        # The result can be None which means that the player doesn't have something in his hand,
        # so we need to check for that
        item, item_template = None, None
        if result is not None:
            item, item_template = result

        return item, item_template

    def __repr__(self):
        return "Player %s with char id %s" % (str(self.name), str(self.character_id))