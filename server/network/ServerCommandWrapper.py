# -*- coding:utf-8 -*-
import json
from common.constants.ServerPackagePrefixes import ServerPackagePrefixes
from common.constants.ServerToClientNetworkCommands import PlayerMovingInfo, ContainerItemContentCommand, \
    ItemUsesUpdateCommand, ItemDeleteCommand, ContainerItemClearCommand, CraftingResultDescriptionByClient, \
    HealthModifierUpdate, WorldObjectMessage, StepableUpdate, WearingMessage, \
    UsingResultMessage, UnwearingMessage, NpcInteraction, EnemyInfo, BulletUpdateMessage, BulletDestructionMessage, \
    WorldObjectDeleteMessage, ItemTransferNotWorkedMessage, PlayerLeftAreaMessage, EnemyStartsAttackMessage, AtNewLevel, \
    GuardDenysAccess, CharacterConditionProperties
from common.helper import send_message
from server.health_modifier.SpecificModifierMapping import SpecificModifierMapping


class ServerCommandWrapper():

    def __init__(self, sock):
        self.sock = sock

    def send_at_new_level(self, level_identifier, player):
        message = AtNewLevel.build_package(level_identifier)
        send_message(self.sock, message, player.get_connection().addr)

    def send_enemy_info(self, enemy, player):
        mc = enemy.get_moving_component()

        if mc.is_moving():
            position = mc.get_interpolated_position()
        else:
            position = mc.get_discrete_position()

        enemy_id = enemy.get_id()
        current_life = enemy.get_current_life_points()
        max_life = enemy.get_max_life_points()

        msg = EnemyInfo.build_package(enemy_id, position, current_life, max_life)
        send_message(self.sock, msg, player.get_connection().addr)

    def send_player_moving_info(self, other_player, player):
        if other_player.get_moving_component().is_moving():
            position = other_player.get_moving_component().get_interpolated_position()
        else:
            position = other_player.get_moving_component().get_discrete_position()

        is_moving = 1 if other_player.get_moving_component().is_moving() else 0
        is_me = 1 if other_player == player else 0

        msg = PlayerMovingInfo.build_package(other_player.get_id(), other_player.get_name(), position, is_moving, is_me)
        send_message(self.sock, msg, player.get_connection().addr)

    def send_container_open_information(self, container, player):
        go_uid = container.get_parent_object_id()
        container_type = container.get_container_type()
        container_shape = container.get_container_shape()

        msg = ServerPackagePrefixes.CONTAINER_OPENING + "%(container_type)s;%(game_object_id)s;" \
                                                   "%(container_shape)s" % {
            "container_type": str(container_type),
            "game_object_id": str(go_uid),
            "container_shape": str(container_shape)}
        print msg
        send_message(self.sock, msg, player.get_connection().addr)

    def send_npc_interaction(self, npc_type, player):
        msg = NpcInteraction.build_package(npc_type)
        send_message(self.sock, msg, player.get_connection().addr)

    def send_guard_denys_access(self, world_object_id_guard, xt, yt, player):
        msg = GuardDenysAccess.build_package(world_object_id_guard, xt, yt)
        send_message(self.sock, msg, player.get_connection().addr)

    def send_container_close_information(self, container, player):
        container_type = container.get_container_type()

        msg = ServerPackagePrefixes.CONTAINER_CLOSE + "%(container_type)s" % {
            "container_type": str(container_type)
        }
        send_message(self.sock, msg, player.get_connection().addr)

    def send_container_item_content(self, container, player):
        go_uid = container.get_parent_object_id()
        container_type = container.get_container_type()

        content = container.get_content()
        positions = container.get_item_root_positions()

        for item in content:
            uid = item.get_id()
            shape = item.get_shape()
            tid = item.get_type_id()
            uses = item.get_num_usages()
            start_pos = positions[uid]
            name = item.name

            msg = ContainerItemContentCommand.build_package(
                container_type=str(container_type),
                game_object_id=str(go_uid),
                item_uid=str(uid),
                name=str(name),
                item_shape=str(shape),
                item_tid=str(tid),
                item_uses=str(uses),
                item_start_position=str(start_pos))
            send_message(self.sock, msg, player.get_connection().addr)

    def update_item_stats(self, list_of_items, player):
        for item in list_of_items:
            uid = item.get_id()
            uses = item.get_num_usages()

            msg = ItemUsesUpdateCommand.build_package(uid, uses)
            send_message(self.sock, msg, player.get_connection().addr)

    def send_delete_item_command(self, list_of_items, player):
        for item in list_of_items:
            uid = item.get_id()

            msg = ItemDeleteCommand.build_package(uid)
            send_message(self.sock, msg, player.get_connection().addr)

    def send_client_can_describe_craft_result_item_type(self, item_type_id, player):
        msg = CraftingResultDescriptionByClient.build_package(item_tid=str(item_type_id))
        send_message(self.sock, msg, player.get_connection().addr)

    def send_container_clear_item_content(self, container, player):
        container_type = container.get_container_type()

        msg = ContainerItemClearCommand.build_package(
            container_type=str(container_type))

        send_message(self.sock, msg, player.get_connection().addr)

    def send_health_modifier(self, player):
        health_modifier = player.get_health_modifier_component()
        modifiers = health_modifier.get_modifiers()

        sending_modifiers = [e for e in modifiers.items()
                             if SpecificModifierMapping.get_specific_modifier_by_type(e[0]).is_visible()]

        msg = HealthModifierUpdate.build_package(modifiers=sending_modifiers)
        send_message(self.sock, msg, player.get_connection().addr)


    def send_character_health_properties(self, character_condition_properties, player):
        msg = CharacterConditionProperties.build_package(character_condition_properties.blurriness,
                                                         character_condition_properties.redness)
        send_message(self.sock, msg, player.get_connection().addr)


    def send_world_object(self, world_object, player):
        area_id = world_object.get_area_id()
        object_id = world_object.get_object_id()
        tileset, tposx, tposy = world_object.get_tile_info()
        eposx, eposy = world_object.get_exact_position()
        visible = world_object.is_visible()
        type = "defaultDummTODOType" #TODO ,world_object.get_type()
        payload = world_object.get_payload()
        msg = WorldObjectMessage.build_package(area_id, object_id, tileset, tposx, tposy, eposx, eposy, visible, type, payload)
        send_message(self.sock, msg, player.get_connection().addr)

    def send_atmospheric_info(self, atmospheric_system, player):
        # Update the weather system on login
        atmospheric_type = atmospheric_system.get_atmospheric_type()
        current_temperature = atmospheric_system.get_temperature()
        event = "WTH%i;%i" % (current_temperature, atmospheric_type)
        send_message(self.sock, event, player.get_connection().addr)

    def send_player_left_area(self, player_which_left, player):
        msg = PlayerLeftAreaMessage.build_package(player_which_left.get_id())
        send_message(self.sock, msg, player.get_connection().addr)

    def send_delete_world_object(self, world_object, player):
        area_id = world_object.get_area_id()
        object_id = world_object.get_object_id()
        msg = WorldObjectDeleteMessage.build_package(area_id, object_id)
        send_message(self.sock, msg, player.get_connection().addr)

    def update_world_objects_for_all_players(self, changed_world_objects, all_players):
        for world_object in changed_world_objects:
            area_id = world_object.get_area_id()
            object_id = world_object.get_object_id()
            tileset, tposx, tposy = world_object.get_tile_info()
            eposx, eposy = world_object.get_exact_position()
            visible = world_object.is_visible()
            type = "defaultDummTODOType" #TODO ,world_object.get_type()
            payload = world_object.get_payload()
            msg = WorldObjectMessage.build_package(area_id, object_id, tileset, tposx, tposy, eposx, eposy, visible, type, payload)
            for player in all_players:
                send_message(self.sock, msg, player.get_connection().addr)


    @staticmethod
    def update_bullet_positions_for_all_players(sock, all_bullets, all_players):
        for bullet in all_bullets:
            bullet_id = bullet.get_bullet_id()
            bullet_x = bullet.get_bullet_x()
            bullet_y = bullet.get_bullet_y()
            msg = BulletUpdateMessage.build_package(bullet_id, bullet_x, bullet_y)
            for player in all_players:
                send_message(sock, msg, player.get_connection().addr)

    def send_destroyed_bullets_to_all_players(self, bullets_marked_destroyed, all_players):
        for bullet in bullets_marked_destroyed:
            bullet_id = bullet.get_bullet_id()
            msg = BulletDestructionMessage.build_package(bullet_id)
            for player in all_players:
                send_message(self.sock, msg, player.get_connection().addr)

    def send_enemies_start_attacking(self, enemy_which_attack, all_players):
        for enemy in enemy_which_attack:
            msg = EnemyStartsAttackMessage.build_package(enemy.get_id())
            for player in all_players:
                send_message(self.sock, msg, player.get_connection().addr)

    def send_stepable_updates_to_players(self, stepables_to_update, all_players):
        for stepable in stepables_to_update:
            active = int(stepable.is_active())
            world_object_id = stepable.get_parent_object_id()
            stepable_update_message = StepableUpdate.build_package(world_object_id, active)
            for player in all_players:
                send_message(self.sock, stepable_update_message, player.get_connection().addr)

    def send_client_is_now_wearing_item_list(self, player):
        wearing_handler = player.get_character_wearing_handler()
        list_of_items = wearing_handler.get_worn_item_values()
        print list_of_items
        for pair in list_of_items:
            item, template = pair
            item_id = item.get_id()
            slot = wearing_handler.get_wearing_type(item)
            wear_message = WearingMessage.build_package(item_id, slot)
            send_message(self.sock, wear_message, player.get_connection().addr)

    def send_client_is_now_wearing_item(self, item_id, player, slot):
        wear_message = WearingMessage.build_package(item_id, slot)
        send_message(self.sock, wear_message, player.get_connection().addr)

    def send_client_is_not_wearing_item_anymore(self, item_id, player):
        unwear_message = UnwearingMessage.build_package(item_id)
        send_message(self.sock, unwear_message, player.get_connection().addr)

    def send_transfer_not_worked(self, item_id, from_c, to_c, player):
        item_pos = from_c.get_item_position(item_id)
        x, y = item_pos
        msg = ItemTransferNotWorkedMessage.build_package(item_id,
                                                   x, y,
                                                   from_c.get_container_type(),
                                                   to_c.get_container_type())
        send_message(self.sock, msg, player.get_connection().addr)

    def send_using_result(self, using_result, player):
        using_result_message = UsingResultMessage.build_package(using_result)
        send_message(self.sock, using_result_message, player.get_connection().addr)