# -*- coding:utf-8 -*-
"""

^^^^^^^^^^^^

.. moduleauthor:: sheepy <sheepy@informatik.uni-hamburg.de>

History:
* 26.01.15: Created (sheepy)

"""
import logging

from client.network.ClientToServerNetworkCommands import ClientWantsToOpenContainerCommand, \
    ClientWantsToCloseContainerCommand, ClientWantsToMoveItem, ClientInteractsForWearingItem
from common.ItemTemplateTags import ItemTemplateTags
from common.constants.ContainerConstants import ContainerConstants
from common.constants.ScriptingConstants import ScriptingConstants
from server.components.StatusModifierQueueElement import StatusModifierQueueElement
from server.health_modifier.HungerThirstModifier import HungerCompensationModifier, ThirstCompensationModifier
from server.constants.constans import AREA_CHANGE, SRV_MOVED, SRV_NO_MOVED, CRAFTING_NOT_POSSIBLE, \
    CRAFTING_SUCCESS_NORMAL, CRAFTING_SUCCESS_DUMMY, GUARD_ALLOWS, GUARD_DENYS, SRV_NO_MOVED_OPEN_CONTAINER, \
    SRV_NO_MOVED_ALREADY_MOVING
from server.world_objects.object_components.AbstractComponent import AbstractComponent
from server.constants.string_constants import GUARD_WALKABLE_TYPE


logger = logging.getLogger(__name__)


class ClientCommandDispatcher():
    def __init__(self, server_command_wrapper):
        self.server_command_wrapper = server_command_wrapper

    def handle_full_data_propagation_to_client(self, all_players, server_level, player, enemy_service,
                                               atmospheric_system, player_update_sim_step_queue):
        # Get the area specification and send them to the client
        level_identifier = server_level.get_level_identifier()
        self.server_command_wrapper.send_at_new_level(level_identifier, player)

        # Get all available objects and send them to the client
        objects = server_level.get_world_object_manager().get_objects()
        for usable_world_object in objects:
            self.server_command_wrapper.send_world_object(usable_world_object, player)

        # Send all player information to the client
        for p in all_players:
            self.server_command_wrapper.send_player_moving_info(p, player)

        for enemy in enemy_service.get_all_enemies():
            self.server_command_wrapper.send_enemy_info(enemy, player)

        self.server_command_wrapper.send_atmospheric_info(atmospheric_system, player)

        # Send all the health modifiers to the player
        self.server_command_wrapper.send_health_modifier(player)
        # Tell the client what he is currently wearing
        self.server_command_wrapper.send_client_is_now_wearing_item_list(player)

        # Add this player to the updates for all others because he is new
        player_update_sim_step_queue.push(player)

    def handle_player_movement(self, server_level, player_service_client, player, open_container_memorizer, info):
        """ This method executes the request of a movement signal coming from the client.
            When the direction the user wants to move to is accessable then the character
            is moved there. If it is not immideadly accessable a check is performed to determine
            if that spot is a change_area_spot which would move the player to another area.
            It returns the result of that to make further processing if necessary. """
        if player.get_moving_component().is_moving():
            return SRV_NO_MOVED_ALREADY_MOVING

        if open_container_memorizer.has_open_container(player):
            logger.info("Player %s cannot move due to open container" % str(player))
            return SRV_NO_MOVED_OPEN_CONTAINER

        # Get the direction the user wants to move towards
        x, y = info.split(";")
        x, y = int(x), int(y)

        direction = (x, y)

        # Get the players position and apply the direction the user wants to go to
        orientation, posx, posy = player.get_moving_component().get_discrete_position()
        x, y = direction
        tx, ty = posx + x, posy + y

        tdirection = orientation
        if x == 1 and y == 0:
            tdirection = 1
        if x == -1 and y == 0:
            tdirection = 2
        if x == 0 and y == 1:
            tdirection = 3
        if x == 0 and y == -1:
            tdirection = 4

        # Check if the position is normally walkable and if so move him and return SRV_MOVED
        walkable_result = server_level.is_walkable(tx, ty)
        # TODO Check the special condition if it is not walkable for the guard type and let the player pass
        # if he has the correct key card

        if walkable_result.is_walkable:
            player.get_moving_component().start_moving((tdirection, tx, ty))
            player_service_client.register_moving_player(player)
            return SRV_MOVED

        # If that field isn't accessable check if its a special change_area_spot
        # and move if so but return AREA_CHANGE
        if server_level.is_change_area_spot(tx, ty):
            player.get_moving_component().start_moving((tdirection, tx, ty))
            player_service_client.register_moving_player(player)
            return AREA_CHANGE

        if walkable_result.walking_blocked_type == GUARD_WALKABLE_TYPE:
            # get the requirements
            npc_component = walkable_result.additional_information
            player_inventory = player.get_inventory()
            is_id_card_correct = player_inventory.has_sufficient_id_card(npc_component.get_guard_type(),
                                                                         npc_component.get_guard_level())

            if is_id_card_correct:
                player.get_moving_component().start_moving((tdirection, tx, ty))
                player_service_client.register_moving_player(player)
                return GUARD_ALLOWS
            else:
                world_object_id_guard = npc_component.get_parent_object_id()
                self.server_command_wrapper.send_guard_denys_access(world_object_id_guard, tx, ty, player)
                return GUARD_DENYS

        # Return that the player hasn't moved at all
        return SRV_NO_MOVED

    def handle_client_wants_to_close_a_container(self, info, open_container_memorizer, player,
                                                 server_level, world_object_deletion_update_queue):
        container_type = ClientWantsToCloseContainerCommand.from_string(info)

        if container_type == ContainerConstants.CONTAINER_TYPE_NORMAL:
            container = open_container_memorizer.get_loot_container_by_player(player)
            if container is not None:
                open_container_memorizer.close_container_for_player(player, container)
                self.server_command_wrapper.send_container_close_information(container, player)
            if container.is_empty() and container.get_vanish_on_empty():
                # TODO Make sure that it is not removed when other players are still accessing it
                wo = server_level.get_world_object_manager().get_world_object_by_id(container.get_parent_object_id())
                world_object_deletion_update_queue.push(wo)

        elif container_type == ContainerConstants.CONTAINER_TYPE_BACKPACK:
            container = player.get_inventory()
            open_container_memorizer.close_container_for_player(player, container)
            self.server_command_wrapper.send_container_close_information(container, player)
        elif container_type == ContainerConstants.CONTAINER_TYPE_CRAFTING:
            container = player.get_crafting_container()
            open_container_memorizer.close_container_for_player(player, container)
            self.server_command_wrapper.send_container_close_information(container, player)

    def handle_client_wants_to_open_a_container(self, info, player, open_container_memorizer, server_level,
                                                item_spawn_service):

        # First get the container type the player wants to open
        container_type = ClientWantsToOpenContainerCommand.from_string(info)

        if container_type == ContainerConstants.CONTAINER_TYPE_NORMAL:

            container = open_container_memorizer.get_loot_container_by_player(player)

            if container is not None:
                return

            # Get the player position
            direction, px, py = player.get_moving_component().get_discrete_position()
            print direction, px, py

            # Check if we can search that spot and if we can do so we get the rarity
            game_object = server_level.can_search_spot(px, py)

            if game_object is None:
                return

            # Get the container of the game object
            container = game_object.get_component(AbstractComponent.CONTAINER_COMPONENT)

            if open_container_memorizer.is_container_already_in_use(container):
                return

            if container.content is None or len(container.content) == 0:
                prepared_container_successfull = item_spawn_service.handle_container(container)

                if prepared_container_successfull:
                    open_container_memorizer.set_container_for_player_opened(player, container)

                    self.server_command_wrapper.send_container_open_information(container, player)
                    self.server_command_wrapper.send_container_item_content(container, player)
            else:
                open_container_memorizer.set_container_for_player_opened(player, container)

                self.server_command_wrapper.send_container_open_information(container, player)
                self.server_command_wrapper.send_container_item_content(container, player)

        elif container_type == ContainerConstants.CONTAINER_TYPE_BACKPACK:
            inventory_container = player.get_inventory()
            open_container_memorizer.set_container_for_player_opened(player, inventory_container)

            self.server_command_wrapper.send_container_open_information(inventory_container, player)
            self.server_command_wrapper.send_container_item_content(inventory_container, player)

        elif container_type == ContainerConstants.CONTAINER_TYPE_CRAFTING:
            crafting_container = player.get_crafting_container()
            open_container_memorizer.set_container_for_player_opened(player, crafting_container)

            self.server_command_wrapper.send_container_open_information(crafting_container, player)
            self.server_command_wrapper.send_container_item_content(crafting_container, player)

    @staticmethod
    def __try_transfer_item(from_c, to_c, item_id_source, item_new_start_pos):
        source_item = from_c.get_item_by_id(item_id_source)

        if source_item is None:
            return False

        if to_c.put_item_if_fits(source_item, item_new_start_pos):
            # Worked so we remove the item from the old container except containers are the same
            if from_c != to_c:
                from_c.remove_item(source_item)

            return True
        else:
            return False

    def handle_client_wants_to_move_item(self, info, player, open_container_memorizer):
        container_type_from, container_type_to, \
            item_id_source, item_new_start_pos = ClientWantsToMoveItem.from_string(info)

        both_containers = open_container_memorizer.get_both_containers_open(player,
                                                                            container_type_from,
                                                                            container_type_to)

        if both_containers is None:
            return

        from_c, to_c = both_containers

        if self.__try_transfer_item(from_c, to_c, item_id_source, item_new_start_pos):
            # Had worked -> notify client that it worked
            logger.info("Transfer of item %s from %s to %s worked" % (str(item_id_source), str(from_c), str(to_c)))
            if from_c.get_container_type() == ContainerConstants.CONTAINER_TYPE_BACKPACK \
                    and not from_c == to_c:
                char_wearing_handler = player.get_character_wearing_handler()
                char_wearing_handler.unwear_item(item_id_source)
                self.server_command_wrapper.send_client_is_not_wearing_item_anymore(item_id_source, player)
        else:
            logger.warn("Transfer of item %s not worked from %s to %s" % (
                str(item_id_source),
                str(from_c),
                str(to_c)))

            self.server_command_wrapper.send_transfer_not_worked(item_id_source,
                                                                 from_c,
                                                                 to_c,
                                                                 player)

    def handle_client_wants_to_use(self, bullet_system, player, server_level):
        # TODO There is maybe a conflict for some items because they could be taken in hand
        # TODO but maybe they could used in some other way ...

        # First of all we need to get the world object that is on the spot the player is
        direction, px, py = player.get_moving_component().get_discrete_position()
        usable_world_object = server_level.get_usable_component_for_spot(px, py)
        npc_world_object = server_level.get_npc_component_for_spot(px, py)

        logger.info("Player %s performed a use command" % str(player))

        if usable_world_object is not None:
            # The player wants probably interact with the world object
            item, item_template = player.get_item_and_item_template_player_has_in_hand()

            # Now we extract the usable component and the call the underlying script
            usable_component = usable_world_object.get_component(AbstractComponent.USABLE_COMPONENT)
            usage_result = usable_component.use(player, item)

            # The result of the script can have several different outcomes
            if usage_result == ScriptingConstants.IN_COOL_DOWN or usage_result is None:
                # We don't send any information at when we are still in cool down time
                logger.info("World Object for player is usable but still in COOL_DOWN")
            else:
                # We send the result to the client
                self.server_command_wrapper.send_using_result(usage_result, player)
        elif npc_world_object is not None:
            # It is an NPC interaction
            npc_component = npc_world_object.get_component(AbstractComponent.NPC_COMPONENT)
            npc_type = npc_component.get_npc_type()
            self.server_command_wrapper.send_npc_interaction(npc_type, player)
        else:
            logger.info("The use can only be resolved into an interaction!")
            # The player may want to interact with an item he is holding in his hand
            item, item_template = player.get_item_and_item_template_player_has_in_hand()

            if item is None or item_template is None:
                # The player just wanted to interact some how but we could not make out why
                logger.info("The player interacted into nothingness - doing nothing at all!")
            else:
                logger.info("The player interacted with items that could mean a thing (%s, %s)!"
                            % (str(item), str(item_template)))
                # The player has an item in his hands and therefore we need to take care
                # of the thing he wants to do with that
                self.__handle_player_wants_to_use_item_solely(bullet_system, player, item, item_template)

    @staticmethod
    def __handle_player_wants_to_use_item_solely(bullet_system, player, item, item_template):
        """ This method handles the use of an item by the player. There are various effects that can occur when
            the player uses an item solely that he holds in his hand - the most general case is to consume it """
        logger.info("The player tries to interact with an item_template which has the following tags: %s"
                    % str(item_template.get_type_set()))

        if item_template.has_tag(ItemTemplateTags.CONSUMABLE):
            # The item is consumable - so we split further into categories
            if item_template.has_tag(ItemTemplateTags.CONSUMES_AS_FOOD):
                hmc = player.get_health_modifier_component()
                hmc.add_status_modifier_to_queue(StatusModifierQueueElement(
                    HungerCompensationModifier(), 0))
                if item.decrease_usage_true_on_zero():
                    item.mark_deleting()
                player.add_item_to_changed_set(item)
            elif item_template.has_tag(ItemTemplateTags.CONSUMES_AS_DRINK):
                hmc = player.get_health_modifier_component()
                hmc.add_status_modifier_to_queue(StatusModifierQueueElement(
                    ThirstCompensationModifier(), 0))
                if item.decrease_usage_true_on_zero():
                    item.mark_deleting()
                player.add_item_to_changed_set(item)

        if item_template.has_tag(ItemTemplateTags.WEAPON):
            #spawn a bullet
            direction, start_posx, start_posy = player.get_moving_component().get_discrete_position()
            bullet_system.add_bullet(direction, start_posx, start_posy)
            # TODO WEAPON SOUND EFFECT AND SO ON

    def handle_client_wants_to_craft(self, player, open_container_memorizer,
                                     crafting_service_client, item_service_client):
        logger.info("Player %s wants to craft!" % str(player))

        if open_container_memorizer.has_open_crafting_container(player):
            result = self.__craft_items_in_container(player, crafting_service_client, item_service_client)

            if result == CRAFTING_NOT_POSSIBLE:
                print "Crafting not possible"

            if result == CRAFTING_SUCCESS_NORMAL or result == CRAFTING_SUCCESS_DUMMY:
                crafting_container = player.get_crafting_container()
                self.server_command_wrapper.send_container_open_information(crafting_container, player)
                self.server_command_wrapper.send_container_clear_item_content(crafting_container, player)
                self.server_command_wrapper.send_container_item_content(crafting_container, player)

                if result == CRAFTING_SUCCESS_DUMMY:
                    content = crafting_container.get_content()
                    assert len(content) == 1

                    item_type_id = content[0].get_type_id()
                    self.server_command_wrapper.send_client_can_describe_craft_result_item_type(item_type_id,
                                                                                                player)

    @staticmethod
    def __craft_items_in_container(player, crafting_service_client, item_service_client):
        container = player.get_crafting_container()

        shape_representation = container.get_representation_for_crafting()

        logger.info("Start crafting for ShapeRepresentation: %s" % str(shape_representation))

        crafting_result = crafting_service_client.process_crafting_request(shape_representation)

        if crafting_result.is_valid_crafting():
            container.shallow_clear()

            resulting_items = crafting_result.get_result()

            complete_items = []
            for element in resulting_items:
                # Instantiate an item and put it into the crafting slot
                item_template, amount = element

                items = item_service_client.create_multiple_items(item_template, amount)

                complete_items += items

            container.set_content(complete_items)
            container.position_content_within_container()

            # TODO Handle the fact that something could go wrong
            if crafting_result.is_crafting_dummy():
                return CRAFTING_SUCCESS_DUMMY
            else:
                return CRAFTING_SUCCESS_NORMAL
        else:
            return CRAFTING_NOT_POSSIBLE

    def handle_client_interacts_for_wearing_item(self, info, player, open_container_memorizer):
        item_id = ClientInteractsForWearingItem.from_string(info)

        if not open_container_memorizer.has_open_inventory_container(player):
            logger.warn("Player %s tried to wear item %s without an open backpack!" % (str(player), str(item_id)))
            return

        inventory = player.get_inventory()
        item = inventory.get_item_by_id(item_id)

        if item is None:
            logger.warn("Player %s tried to wear item %s which could not be found in his backpack!"
                        % (str(player), str(item_id)))
            return

        wearing_handler = player.get_character_wearing_handler()

        # If the item is worn take it of - if it is not worn put it on
        if wearing_handler.is_item_worn(item_id):
            wearing_handler.unwear_item(item_id)
            self.server_command_wrapper.send_client_is_not_wearing_item_anymore(item_id, player)
        else:
            if wearing_handler.try_wearing_item(item):
                slot = wearing_handler.get_wearing_type(item)
                self.server_command_wrapper.send_client_is_now_wearing_item(item_id, player, slot)
            else:
                # TODO - We should inform the player why he could not wear it or make it such that the item is swapped
                logger.warn("Player %s tried to wear item %s but was not possible!" % (str(player), str(item)))
