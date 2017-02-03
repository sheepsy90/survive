# -*- coding:utf-8 -*-
from common.ItemTemplateTags import ItemTemplateTagConsistencyChecker
from common.LevelLoader import LevelFactory
from server.level.FullServerLevel import FullServerLevel


def load_level_for_server(map_file):
    ItemTemplateTagConsistencyChecker.check()
    level_factory = LevelFactory()
    level_template = level_factory.load_level(map_file)
    objects = level_template.build_objects()
    area_transitions = level_template.build_area_transitions()
    enemies = level_template.build_enemies()
    scripts = level_template.build_internal_scripts()
    atmospheric_data = level_template.get_atmospheric_data()
    full_server_level = FullServerLevel(level_template.get_identifier(),
                                        level_template.get_size(),
                                        objects,
                                        scripts,
                                        enemies,
                                        level_template.build_walk_map(),
                                        level_template.build_robot_follow_map(),
                                        atmospheric_data,
                                        area_transitions)
    return full_server_level

