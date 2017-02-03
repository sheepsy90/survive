import json
import logging
import time
from client.drawers.BasicEffectDrawer import EffectObject, GuardDenysEffect
from client.logic.ShallowItem import ShallowItem
from common.constants.ContainerConstants import ContainerConstants
from common.constants.ServerPackagePrefixes import ServerPackagePrefixes
from common.constants.ServerToClientNetworkCommands import UsingResultMessage, \
    ContainerItemContentCommand, ContainerItemClearCommand, CraftingResultDescriptionByClient,\
    HealthModifierUpdate, \
    WorldObjectMessage, StepableUpdate, WearingMessage, \
    UnwearingMessage, ItemUsesUpdateCommand, \
    PlayerMovingInfo, ItemDeleteCommand, NpcInteraction, EnemyInfo, BulletUpdateMessage, BulletDestructionMessage, \
    WorldObjectDeleteMessage, ItemTransferNotWorkedMessage, EnemyStartsAttackMessage, NewConnectionMessage, AtNewLevel, \
    GuardDenysAccess, CharacterConditionProperties, PlayerLeftAreaMessage

logger = logging.getLogger(__name__)


class ServerCommandDispatcher():

    def __init__(self, state_machine, client_level_manager, sound_engine, client_socket_wrapper, looting_manager,
                 backpack_manager, crafting_manager, description_manager, wearing_manager,
                 npc_system, effect_list):
        self.state_machine = state_machine
        self.client_level_manager = client_level_manager
        self.sound_engine = sound_engine
        self.client_socket_wrapper = client_socket_wrapper

        self.looting_manager = looting_manager
        self.backpack_manager = backpack_manager
        self.crafting_manager = crafting_manager
        self.general_item_watcher = client_level_manager.get_general_item_watcher()

        self.wearing_manager = wearing_manager
        self.description_manager = description_manager
        self.npc_system = npc_system
        self.effect_list = effect_list

    def get_manager_by_type(self, to_type):
        manager_from = None
        if to_type == ContainerConstants.CONTAINER_TYPE_BACKPACK:
            manager_from = self.backpack_manager
        if to_type == ContainerConstants.CONTAINER_TYPE_CRAFTING:
            manager_from = self.crafting_manager
        if to_type == ContainerConstants.CONTAINER_TYPE_NORMAL:
            manager_from = self.looting_manager
        return manager_from

    def dispatch_server_instruction(self, command, info):

        if command == WorldObjectMessage.prefix():
            area_id, object_id, tileset, tposx, tposy, eposx, eposy, visible, type, payload = WorldObjectMessage.from_string(info)
            print "GOT TYPE", type
            print "GOT PAYLOAD", payload
            payload = json.loads(payload)
            obj_mgr = self.client_level_manager.get_current_level().get_object_manager()
            obj_mgr.add_to_objects(area_id, object_id, tileset, tposx, tposy, eposx, eposy, visible, type, payload)
            return

        if command == WorldObjectDeleteMessage.prefix():
            area_id, object_id = WorldObjectDeleteMessage.from_string(info)
            obj_mgr = self.client_level_manager.get_current_level().get_object_manager()
            obj_mgr.remove(area_id, object_id)
            return

        if command == StepableUpdate.prefix():
            world_object_id, active = StepableUpdate.from_string(info)
            obj_mgr = self.client_level_manager.get_current_level().get_object_manager()
            obj_mgr.update_stepable_object(world_object_id, active)
            return

        if command == AtNewLevel.prefix():
            """ This command delivers a new level_identifier of the level the client needs to load """
            area_id = AtNewLevel.from_string(info)
            self.client_level_manager.set_level_identifier(area_id)
            return

        if command == PlayerMovingInfo.prefix():
            player_id, player_name, d, x, y, is_moving, is_me = PlayerMovingInfo.from_string(info)
            player_manager = self.client_level_manager.get_current_level().get_player_manager()
            player_manager.add_new_player_position(player_id, player_name, (d, x, y), is_moving, is_me)
            return

        if command == NpcInteraction.prefix():
            npc_type = NpcInteraction.from_string(info)
            self.npc_system.interaction_with_npc_type(npc_type)
            return

        if command == GuardDenysAccess.prefix():
            wo_id, xt, yt = GuardDenysAccess.from_string(info)
            eo = GuardDenysEffect(wo_id, xt, yt)
            self.effect_list.__add__(eo)
            self.sound_engine.play("not_authorized", single_mode=True)
            return

        if command == PlayerLeftAreaMessage.prefix():
            player_id = PlayerLeftAreaMessage.from_string(info)
            player_manager = self.client_level_manager.get_current_level().get_player_manager()
            player_manager.remove_player(player_id)

        if command == EnemyInfo.prefix():
            enemy_id, d, x, y, current_life, max_life = EnemyInfo.from_string(info)
            client_enemy_manager = self.client_level_manager.get_current_level().get_client_enemy_manager()
            client_enemy_manager.update_enemy(enemy_id, d, x, y, current_life, max_life)
            return

        if command == EnemyStartsAttackMessage.prefix():
            enemy_id = EnemyStartsAttackMessage.from_string(info)
            client_enemy_manager = self.client_level_manager.get_current_level().get_client_enemy_manager()
            client_enemy_manager.enemy_starts_attacking(enemy_id)
            return

        if command == CharacterConditionProperties.prefix():
            blurriness, redness = CharacterConditionProperties.from_string(info)
            player_manager = self.client_level_manager.get_current_level().get_player_manager()
            player_manager.set_my_character_condition(blurriness, redness)
            return

        if command == NewConnectionMessage.prefix():
            is_still_tutorial, new_ip, new_port = NewConnectionMessage.from_string(info)
            logger.info("NewConnectionMessage - StillTut: {}, New IP/Port: {}:{}"
                        .format(is_still_tutorial, new_ip, new_port))

            self.client_socket_wrapper.set_new_connection_info(new_ip, int(new_port))
            self.state_machine.set_character_is_still_tutorial(is_still_tutorial)
            self.state_machine.set_connected(False)

            #TODO This is a client side fix - the problem is that the transition soemtimes trashes an area
            # probably due to some service sync thingy
            time.sleep(1)
            return

        if command == BulletUpdateMessage.prefix():
            bullet_id, x, y = BulletUpdateMessage.from_string(info)
            bullet_manager = self.client_level_manager.get_current_level().get_bullet_manager()
            bullet_manager.add_bullet(bullet_id, x, y)
            return

        if command == BulletDestructionMessage.prefix():
            bullet_id = BulletDestructionMessage.from_string(info)
            bullet_manager = self.client_level_manager.get_current_level().get_bullet_manager()
            bullet_manager.bullet_destroyed(bullet_id)
            return

        if command == CraftingResultDescriptionByClient.prefix():
            item_type_id = CraftingResultDescriptionByClient.from_string(info)

            self.description_manager.set_description_possibility(item_type_id)

            return

        if command == UsingResultMessage.prefix():
            # This shall result in something and we need to get it by the tutorial state machine
            using_result = UsingResultMessage.from_string(info)
            self.client_level_manager.get_using_history().add_using_entry(using_result)
            return

        if command == ContainerItemContentCommand.prefix():
            """ This command is used when an item information is passed to the client """
            container_type, game_object_id, item_uid, name,\
            item_shape, item_tid, item_uses, item_start_position = ContainerItemContentCommand.from_string(info)

            shallow_item = ShallowItem(game_object_id, item_uid, name, item_shape, item_tid, item_uses, item_start_position)

            self.general_item_watcher[shallow_item.get_uid()] = shallow_item

            if container_type == ContainerConstants.CONTAINER_TYPE_BACKPACK:
                self.backpack_manager.add_shallow_item(shallow_item)

            if container_type == ContainerConstants.CONTAINER_TYPE_CRAFTING:
                self.crafting_manager.add_shallow_item(shallow_item)

            if container_type == ContainerConstants.CONTAINER_TYPE_NORMAL:
                self.looting_manager.add_shallow_item(shallow_item)
            return

        if command == ItemUsesUpdateCommand.prefix():
            item_id, new_usages = ItemUsesUpdateCommand.from_string(info)
            if item_id not in self.general_item_watcher:
                print "Update for item not in general watcher - dismiss", item_id
            else:
                self.general_item_watcher[item_id].set_item_uses(new_usages)
            return

        if command == ItemDeleteCommand.prefix():
            item_id = ItemDeleteCommand.from_string(info)
            self.general_item_watcher[item_id].mark_deleted()
            return

        if command == ServerPackagePrefixes.CONTAINER_OPENING:
            # TODO Add the information if the container is read only and if so make the adjsutments such that the client is
            # able to recognize that it is not possible to move the item
            data = info.split(";")
            container_type = int(data[0])
            go_uid = data[1]
            container_shape = eval(data[2])

            if container_type == ContainerConstants.CONTAINER_TYPE_BACKPACK:
                self.backpack_manager.open(container_shape)

            if container_type == ContainerConstants.CONTAINER_TYPE_CRAFTING:
                self.crafting_manager.open(container_shape)

            if container_type == ContainerConstants.CONTAINER_TYPE_NORMAL:
                go_uid = int(go_uid)
                self.looting_manager.open_container(go_uid, container_shape)
            return

        if command == ItemTransferNotWorkedMessage.prefix():
            item_id, x, y, from_type, to_type = ItemTransferNotWorkedMessage.from_string(info)
            print "Item Transfer not worked", item_id, x, y, from_type, to_type
            # We need to reverse the item

            to_manager = self.get_manager_by_type(to_type)
            from_manager = self.get_manager_by_type(from_type)

            if from_manager is not None and to_manager is not None:
                shallow_item = to_manager.get_item_by_id(item_id)
                to_manager.remove_item_local(item_id)
                shallow_item.item_start_position = (x, y)
                from_manager.add_shallow_item(shallow_item)
            else:
                print "Could not reverse item to its original position"

        if command == ServerPackagePrefixes.CONTAINER_CLOSE:
            data = info.split(";")
            container_type = int(data[0])

            if container_type == ContainerConstants.CONTAINER_TYPE_BACKPACK:
                self.backpack_manager.close()

            if container_type == ContainerConstants.CONTAINER_TYPE_CRAFTING:
                self.crafting_manager.close()

            if container_type == ContainerConstants.CONTAINER_TYPE_NORMAL:
                self.looting_manager.close_container()
            return

        if command == WearingMessage.prefix():
            item_id, slot = WearingMessage.from_string(info)
            self.wearing_manager.add_item_wearing(item_id, slot)
            print "Client wears now", item_id, "on slots", slot
            return

        if command == UnwearingMessage.prefix():
            item_id = UnwearingMessage.from_string(info)
            self.wearing_manager.remove_item_wearing(item_id)
            print "Client wears not anymore", item_id
            return

        if command == ContainerItemClearCommand.prefix():
            container_type = ContainerItemClearCommand.from_string(info)

            if container_type == ContainerConstants.CONTAINER_TYPE_BACKPACK:
                self.backpack_manager.clear()

            if container_type == ContainerConstants.CONTAINER_TYPE_CRAFTING:
                self.crafting_manager.clear()

            if container_type == ContainerConstants.CONTAINER_TYPE_NORMAL:
                self.looting_manager.clear()
            return

        if command == "WTH":
            current_temperature, atmospheric_type = info.split(';')
            level = self.client_level_manager.get_current_level()

            ws = level.get_atmospheric_system()
            ws.set_temperature(int(current_temperature))
            ws.set_atmospheric_type(int(atmospheric_type))
            return

        if command == 'RJC':
            # TODO - Go back to the Character Selection
            print "Server Rejected Connection"
            return

        if command == HealthModifierUpdate.prefix():
            level = self.client_level_manager.get_current_level()
            hm = level.get_health_modifier_manager()

            mod_list = HealthModifierUpdate.from_string(info)
            for e in mod_list:
                hm.update_health_mod(e[0], e[1])
            return

        print "Not processed", command, info