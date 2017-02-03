# -*- coding:utf-8 -*-
import json
from common.constants.ServerPackagePrefixes import ServerPackagePrefixes

LOOK_RIGHT = 1
LOOK_LEFT = 2
LOOK_DOWN = 3
LOOK_UP = 4


class ContainerItemContentCommand():

    @staticmethod
    def build_package(container_type, game_object_id, item_uid, name, item_shape,
                        item_tid, item_uses, item_start_position):
        return ContainerItemContentCommand.prefix() + ";".join([container_type, game_object_id, item_uid, name,
                        item_shape, item_tid, item_uses, item_start_position])

    @staticmethod
    def from_string(string):
        container_type, game_object_id, item_uid, name, \
            item_shape, item_tid, item_uses, item_start_position = string.split(";")
        return int(container_type), game_object_id, int(item_uid), name, \
            eval(item_shape), int(item_tid), int(item_uses), eval(item_start_position)

    @staticmethod
    def prefix():
        return ServerPackagePrefixes.CONTAINER_ITEM_CONTENT


class CraftingResultDescriptionByClient():

    @staticmethod
    def build_package(item_tid):
        return CraftingResultDescriptionByClient.prefix() + ";".join([item_tid])

    @staticmethod
    def from_string(string):
        return int(string)

    @staticmethod
    def prefix():
        return ServerPackagePrefixes.CRAFTING_RESULT_DESCRIPTION_BY_CLIENT


class ContainerItemClearCommand():

    @staticmethod
    def build_package(container_type):
        return ContainerItemClearCommand.prefix() + ";".join([container_type])

    @staticmethod
    def from_string(string):
        return int(string)

    @staticmethod
    def prefix():
        return ServerPackagePrefixes.CONTAINER_ITEM_CLEAR_CONTENT

class CharacterConditionProperties():

    @staticmethod
    def build_package(blurriness, redness):
        return CharacterConditionProperties.prefix() + ";".join([str(blurriness), str(redness)])

    @staticmethod
    def from_string(string):
        blurriness, redness = string.split(";")
        return int(blurriness), int(redness)

    @staticmethod
    def prefix():
        return ServerPackagePrefixes.CHARACTER_CONDITION_PROPERTIES

class HealthModifierUpdate():

    @staticmethod
    def build_package(modifiers):
        sending_modifiers = [str(e[0]) + ";" + str(e[1]) for e in modifiers]
        return HealthModifierUpdate.prefix() + "#".join(sending_modifiers)

    @staticmethod
    def from_string(string):
        if string == "":
            return []
        elements = string.split("#")
        elementwise = [e.split(";") for e in elements]
        elementwise = [[int(e[0]), int(e[1])] for e in elementwise]
        return elementwise

    @staticmethod
    def prefix():
        return ServerPackagePrefixes.HEALTH_MODIFIER_UPDATE

class WorldObjectMessage():

    @staticmethod
    def build_package(area_id, object_id, tileset, tposx, tposy, eposx, eposy, visible, type, payload):
        return WorldObjectMessage.prefix() + ";".join([str(area_id), str(object_id), tileset, str(tposx), str(tposy), str(eposx), str(eposy), str(visible), type, json.dumps(payload)])

    @staticmethod
    def from_string(string):
        area_id, object_id, tileset, tposx, tposy, eposx, eposy, visible, type, payload = string.split(";")
        return int(area_id), int(object_id), tileset, int(tposx), int(tposy), int(eposx), int(eposy), visible == "True", type, payload

    @staticmethod
    def prefix():
        return ServerPackagePrefixes.WORLD_OBJECT_MESSAGE


class PlayerLeftAreaMessage():

    @staticmethod
    def build_package(player_id):
        return PlayerLeftAreaMessage.prefix() + str(player_id)

    @staticmethod
    def from_string(string):
        return int(string)

    @staticmethod
    def prefix():
        return ServerPackagePrefixes.PLAYER_LEFT_AREA


class WorldObjectDeleteMessage():

    @staticmethod
    def build_package(area_id, object_id):
        return WorldObjectDeleteMessage.prefix() + ";".join([str(area_id), str(object_id)])

    @staticmethod
    def from_string(string):
        area_id, object_id = string.split(";")
        return int(area_id), int(object_id)

    @staticmethod
    def prefix():
        return ServerPackagePrefixes.WORLD_OBJECT_DELETE_MESSAGE



class BulletUpdateMessage():

    @staticmethod
    def build_package(bullet_id, x, y):
        return BulletUpdateMessage.prefix() + ";".join([str(bullet_id), str(x), str(y)])

    @staticmethod
    def from_string(string):
        bullet_id, x, y = string.split(";")
        return int(bullet_id), float(x),  float(y)

    @staticmethod
    def prefix():
        return ServerPackagePrefixes.BULLET_UPDATE_MESSAGE


class NewConnectionMessage():

    @staticmethod
    def build_package(is_still_tutorial, new_ip, new_port):
        return NewConnectionMessage.prefix() + ";".join([str(is_still_tutorial), new_ip, str(new_port)])

    @staticmethod
    def from_string(string):
        is_still_tutorial, new_ip, new_port = string.split(";")
        return int(is_still_tutorial) == 1, new_ip, int(new_port)

    @staticmethod
    def prefix():
        return ServerPackagePrefixes.NEW_CONNECTION_MESSAGE


class EnemyStartsAttackMessage():

    @staticmethod
    def build_package(enemy_id):
        return EnemyStartsAttackMessage.prefix() + str(enemy_id)

    @staticmethod
    def from_string(string):
        return int(string)

    @staticmethod
    def prefix():
        return ServerPackagePrefixes.ENEMY_STARTS_ATTACK_MESSAGE


class BulletDestructionMessage():

    @staticmethod
    def build_package(bullet_id):
        return BulletDestructionMessage.prefix() + str(bullet_id)

    @staticmethod
    def from_string(string):
        return int(string)

    @staticmethod
    def prefix():
        return ServerPackagePrefixes.BULLET_DESTRUCTION_MESSAGE

class StepableUpdate():

    @staticmethod
    def build_package(world_object_id, active):
        return StepableUpdate.prefix() + ";".join([str(world_object_id), str(active)])

    @staticmethod
    def from_string(string):
        world_object_id, active = string.split(";")
        return int(world_object_id), int(active)

    @staticmethod
    def prefix():
        return ServerPackagePrefixes.STEPABLE_UPDATE


class AtNewLevel():

    @staticmethod
    def build_package(area_id):
        return AtNewLevel.prefix() + str(area_id)

    @staticmethod
    def from_string(string):
        return int(string)

    @staticmethod
    def prefix():
        return ServerPackagePrefixes.AT_NEW_LEVEL


class WearingMessage():

    @staticmethod
    def build_package(item_id, slot):
        return WearingMessage.prefix() + ";".join([str(item_id), str(slot)])

    @staticmethod
    def from_string(string):
        item_id, slot = string.split(";")
        return int(item_id), str(slot)

    @staticmethod
    def prefix():
        return ServerPackagePrefixes.WEARING_MESSAGE


class UnwearingMessage():

    @staticmethod
    def build_package(item_id):
        return UnwearingMessage.prefix() + str(item_id)

    @staticmethod
    def from_string(string):
        return int(string)

    @staticmethod
    def prefix():
        return ServerPackagePrefixes.UNWEARING_MESSAGE


class ItemTransferNotWorkedMessage():

    @staticmethod
    def build_package(item_id, x, y, from_type, to_type):
        return ItemTransferNotWorkedMessage.prefix() + ";".join([str(item_id), str(x), str(y), str(from_type), str(to_type)])

    @staticmethod
    def from_string(string):
        item_id, x, y, from_type, to_type = string.split(";")
        return int(item_id), int(x), int(y), int(from_type), int(to_type)

    @staticmethod
    def prefix():
        return ServerPackagePrefixes.ITEM_TRANSFER_NOT_WORKED

class UsingResultMessage():

    @staticmethod
    def build_package(using_result):
        return UsingResultMessage.prefix() + str(using_result)

    @staticmethod
    def from_string(using_result):
        return int(using_result)

    @staticmethod
    def prefix():
        return ServerPackagePrefixes.USING_RESULT_MESSAGE


class ItemUsesUpdateCommand():

    @staticmethod
    def build_package(item_id, new_usage_number):
        return ItemUsesUpdateCommand.prefix() + ";".join([str(item_id), str(new_usage_number)])

    @staticmethod
    def from_string(string):
        item_id, new_num_usages = string.split(";")
        return int(item_id), int(new_num_usages)

    @staticmethod
    def prefix():
        return ServerPackagePrefixes.ITEMS_USES_UPDATE_COMMAND


class ItemDeleteCommand():

    @staticmethod
    def build_package(item_id):
        return ItemDeleteCommand.prefix() + str(item_id)

    @staticmethod
    def from_string(string):
        return int(string)

    @staticmethod
    def prefix():
        return ServerPackagePrefixes.ITEM_DELETE_COMMAND


class PlayerMovingInfo():

    @staticmethod
    def build_package(player_id, player_name, position, is_moving, is_me):
        d, x, y = position
        return PlayerMovingInfo.prefix() + ";".join([str(player_id), str(player_name), str(d), str(x), str(y), str(is_moving), str(is_me)])

    @staticmethod
    def from_string(string):
        player_id, player_name, d, x, y, is_moving, is_me = string.split(";")
        return int(player_id), player_name, int(float(d)), float(x), float(y), int(is_moving), int(is_me)

    @staticmethod
    def prefix():
        return ServerPackagePrefixes.PLAYER_MOVING_INFO


class EnemyInfo():

    @staticmethod
    def build_package(enemy_id, position, current_life, max_life):
        d, x, y = position
        return EnemyInfo.prefix() + ";".join([str(enemy_id), str(d), str(x), str(y), str(current_life), str(max_life)])

    @staticmethod
    def from_string(string):
        player_id, d, x, y, current_life, max_life = string.split(";")
        return int(player_id), int(float(d)), float(x), float(y), int(current_life), int(max_life)

    @staticmethod
    def prefix():
        return ServerPackagePrefixes.ENEMY_INFO

class NpcInteraction():

    @staticmethod
    def build_package(npc_type):
        return NpcInteraction.prefix() + str(npc_type)

    @staticmethod
    def from_string(string):
        return int(string)

    @staticmethod
    def prefix():
        return ServerPackagePrefixes.NPC_INTERACTION


class GuardDenysAccess():

    @staticmethod
    def build_package(world_object_id_guard, xt, yt):
        return GuardDenysAccess.prefix() + ";".join([str(world_object_id_guard), str(xt), str(yt)])

    @staticmethod
    def from_string(string):
        world_object_id_guard, xt, yt = string.split(";")
        return int(world_object_id_guard), int(xt), int(yt)

    @staticmethod
    def prefix():
        return ServerPackagePrefixes.GUARD_DENYS_ACCESS