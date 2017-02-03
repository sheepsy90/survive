# -*- coding:utf-8 -*-
import logging
from common.named_tuples import CharacterConditionProperties
from server.constants.constans import EnemySystemQueueConstants
from server.health_modifier.SpecifiedModifiers import AtmosphericPoison
from server.local_services.AtmosphericSystem import AtmosphericSystem

from server.local_services.SimulationStepObjectBufferQueueSystem import SimulationStepBufferQueue
from server.world_objects.object_components.AbstractComponent import AbstractComponent

logger = logging.getLogger(__name__)


class GameLogicSimulationMethods():

    def __init__(self, server_command_wrapper, simulation_step_buffer_queue_system, server_level,
                 item_service_client, atmospheric_system):
        self.simulation_step_buffer_queue_system = simulation_step_buffer_queue_system
        self.server_command_wrapper = server_command_wrapper
        self.server_level = server_level
        self.item_service_client = item_service_client
        self.atmospheric_system = atmospheric_system
        pass

    def consume_simulation_step_buffer_queue_system(self, all_players):
        """ This is the method which consumes the Sim Step Buffer Queue """

        ''' Those are the real sending methods to propagate player movements '''
        for moved_players in self.simulation_step_buffer_queue_system.get_queue_content(
                SimulationStepBufferQueue.PLAYER_UPDATE):
            for player in all_players:
                self.server_command_wrapper.send_player_moving_info(moved_players, player)

        ''' Process the World Objects that have changed state '''
        changed_world_objects = self.simulation_step_buffer_queue_system.\
            get_queue_content(SimulationStepBufferQueue.WORLD_OBJECTS_CHANGED)
        self.server_command_wrapper.update_world_objects_for_all_players(changed_world_objects, all_players)

        ''' Process the World Objects that where deleted '''
        deleted_world_objects = self.simulation_step_buffer_queue_system.\
            get_queue_content(SimulationStepBufferQueue.WORLD_OBJECTS_DELETED)

        if len(deleted_world_objects) > 0:
            logger.info("Need to Delete of WorldObjects: " + str(deleted_world_objects))

        for element in deleted_world_objects:
            self.server_level.delete_world_object(element)
            for player in all_players:
                self.server_command_wrapper.send_delete_world_object(element, player)

        ''' Process changed enemies '''
        enemies_which_changed = self.simulation_step_buffer_queue_system.\
            get_queue_content(EnemySystemQueueConstants.CHANGED_ENEMIES)
        # Move and update all zombies
        for enemy in enemies_which_changed:
            # TODO we can save computing time here by precalculating the message - its just for capsule reasons within
            # the wrapper
            for player in all_players:
                self.server_command_wrapper.send_enemy_info(enemy, player)

        ''' Process the Players which Left the Area '''
        for player_which_left in self.simulation_step_buffer_queue_system.get_queue_content(
                SimulationStepBufferQueue.PLAYER_LEFT_AREA):
            for player in all_players:
                self.server_command_wrapper.send_player_left_area(player_which_left, player)

        ''' Clear the queues '''
        self.simulation_step_buffer_queue_system.clear_all()

    def update_steppable_components(self, all_players):
        # Check the stepable things
        stepables = self.server_level.get_stepables()
        player_positions = [player.get_moving_component().get_discrete_position() for player in all_players]
        player_positions = [(e[1], e[2]) for e in player_positions]
        stepables_to_update = []
        stepables_world_obj_ids = []
        for usable_world_object in stepables.values():
            # TODO The position oft the footpoint is calculated again and again so maybe it should be saved somewhere
            stepable_component = usable_world_object.get_component(AbstractComponent.STEPABLE_COMPONENT)
            ref_pos = stepable_component.get_reference_position()
            state = ref_pos in player_positions
            if stepable_component.update(state):
                # The state changed so we need to update the client
                stepables_to_update.append(stepable_component)
                stepables_world_obj_ids.append(usable_world_object.get_object_id())
        self.server_command_wrapper.send_stepable_updates_to_players(stepables_to_update, all_players)


        # Handle the Stepping Rules
        stepping_rules = self.server_level.get_stepping_rules()
        for rule in stepping_rules:
            preconditions = rule.get_required_stepable_object_ids()
            need_update_check = len([e for e in preconditions if e in stepables_world_obj_ids]) > 0
            if need_update_check:
                cumulated_active = True
                for element in preconditions:
                    usable_world_object = self.server_level.get_world_object_by_id(element)
                    stepable_componet = usable_world_object.get_component(AbstractComponent.STEPABLE_COMPONENT)
                    if not stepable_componet.is_active():
                        cumulated_active = False
                        break

                if rule.change_state(cumulated_active):
                    # State has changed so we need to do an update
                    target_object_ids = rule.get_visibility_effected_object_ids()
                    for ids in target_object_ids:
                        usable_world_object = self.server_level.get_world_object_by_id(ids)
                        if usable_world_object.set_visible(not cumulated_active):
                            # State changed so wee need to tell the client that
                            self.simulation_step_buffer_queue_system\
                                .push(SimulationStepBufferQueue.WORLD_OBJECTS_CHANGED, usable_world_object)

    def update_health_modifier(self, all_players):
        if self.atmospheric_system.get_atmospheric_type() == AtmosphericSystem.HOSTILE:
            # We have a hostile atmosphere so we need to check if players have masks on
            for player in all_players:
                health_modifier = player.get_health_modifier_component()
                health_modifier.set_modifier(AtmosphericPoison.TYPE_ID, 1)
        else:
            for player in all_players:
                health_modifier = player.get_health_modifier_component()
                health_modifier.unset_modifier(AtmosphericPoison.TYPE_ID)

        # This part handles all modifiers the player has and makes the interconnections between them executing
        for player in all_players:
            health_modifier = player.get_health_modifier_component()
            health_modifier.update()

            # Before we send the health modifiers we need to check the health state of the player -
            # when to much occurred he is dead

            character_condition_properties = self.calculate_character_condition_properties(player)

            if character_condition_properties.alive:
                self.server_command_wrapper.send_character_health_properties(character_condition_properties, player)
                self.server_command_wrapper.send_health_modifier(player)
            else:
                # TODO Handle death
                pass


    def update_items_for_client(self, all_players):
        """ Update the item properties for all players individually """
        for player in all_players:
            items_changed = player.get_items_changed_during_iteration()
            items_needing_update = [e for e in items_changed if not e.is_marked_for_deletion()]
            items_needing_delete = [e for e in items_changed if e.is_marked_for_deletion()]
            self.server_command_wrapper.update_item_stats(items_needing_update, player)
            self.server_command_wrapper.send_delete_item_command(items_needing_delete, player)

            # TODO Handle DELETE ITEM - Carfeul its designed for tutorial level right now
            inventory = player.get_inventory()
            wearing_handler = player.get_character_wearing_handler()
            for item in items_needing_delete:
                inventory.remove_item(item)
                wearing_handler.unwear_item(item.get_id())
                self.item_service_client.delete_item(item.get_id())
            player.clear_items_changed_during_iteration()

    def calculate_character_condition_properties(self, player):
        """ This method looks at all the status modifiers the player has and decides from that in which condition he is
            if he goes over a certain condition that means death. Else it could just be some reduction in sight. """
        #TODO This could need a chace method so we don't need to consider all again on the same input
        health_modifiers = player.get_health_modifier_component().get_modifiers()

        total_num_modifiers = sum(health_modifiers.values())
        _redness = total_num_modifiers*2
        _blurriness = total_num_modifiers/3

        return CharacterConditionProperties(alive=True, blurriness=_blurriness, redness=_redness)

    def handle_script_schedule(self):
        self.server_level.get_intern_script_manager().resolve_script_schedule()