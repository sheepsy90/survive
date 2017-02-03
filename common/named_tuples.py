# -*- coding:utf-8 -*-
from collections import namedtuple

NpcComponentProperties = namedtuple('LevelLoadNpcProperties', ['npc_type',
                                                               'is_guard',
                                                               'npc_guard_type',
                                                               'npc_guard_orientation',
                                                               'npc_guard_level'])


WalkableResult = namedtuple('WalkableResult', ['is_walkable',
                                               'walking_blocked_type',
                                               'additional_information'])


IDSystemStats = namedtuple('IDSystemStats', ['security',
                                         'administration',
                                         'technician',
                                         'science'])

CharacterConditionProperties = namedtuple('CharacterConditionProperties', ['alive',
                                                                           'blurriness',
                                                                           'redness'])


ScriptScheduleElement = namedtuple('ScriptScheduleElement', ['script_id',
                                                             'execution_time'])