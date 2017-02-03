# -*- coding:utf-8 -*-

import logging
from common.ItemTemplateTags import ItemTemplateTags
from common.named_tuples import IDSystemStats
from server.world_objects.object_components.NpcComponent import NpcComponent

logger = logging.getLogger(__name__)


class IdSystemValidator():

    security_tags = [ItemTemplateTags.SECURITY_1, ItemTemplateTags.SECURITY_2, ItemTemplateTags.SECURITY_3]
    technician_tags = [ItemTemplateTags.TECHNICIAN_1, ItemTemplateTags.TECHNICIAN_2, ItemTemplateTags.TECHNICIAN_3]
    administration_tags = [ItemTemplateTags.ADMINISTRATION_1, ItemTemplateTags.ADMINISTRATION_2, ItemTemplateTags.ADMINISTRATION_3]
    science_tags = [ItemTemplateTags.SCIENCE_1, ItemTemplateTags.SCIENCE_2, ItemTemplateTags.SCIENCE_3]

    @staticmethod
    def is_requirement_met(item_template, id_system_stats):
        security_allowed = IdSystemValidator.is_category_allowed(id_system_stats.security, IdSystemValidator.security_tags, item_template)
        technician_allowed = IdSystemValidator.is_category_allowed(id_system_stats.technician, IdSystemValidator.technician_tags, item_template)
        administration_allowed = IdSystemValidator.is_category_allowed(id_system_stats.administration, IdSystemValidator.administration_tags, item_template)
        science_allowed = IdSystemValidator.is_category_allowed(id_system_stats.science, IdSystemValidator.science_tags, item_template)

        return security_allowed and technician_allowed and administration_allowed and science_allowed

    @staticmethod
    def is_category_allowed(requirement, item_template_tag_levels, item_template):
        lvl1, lvl2, lvl3 = item_template_tag_levels
        allowed = True
        if requirement == 1:
            allowed = item_template.has_tag(lvl1) or \
                                item_template.has_tag(lvl2) or \
                                item_template.has_tag(lvl3)
        elif requirement == 2:
            allowed = item_template.has_tag(lvl2) or \
                                item_template.has_tag(lvl3)
        elif requirement == 3:
            allowed = item_template.has_tag(lvl3)

        return allowed

    @staticmethod
    def create_id_system_stats(guard_type, guard_level):
        sec, adm, tec, sci = 0, 0, 0, 0
        if guard_type == NpcComponent.GUARD_TYPE_SECURITY:
            sec = guard_level
        elif guard_type == NpcComponent.GUARD_TYPE_ADMINISTRATION:
            adm = guard_level
        elif guard_type == NpcComponent.GUARD_TYPE_TECHNICIAN:
            tec = guard_level
        elif guard_type == NpcComponent.GUARD_TYPE_SCIENCE:
            sci = guard_level
        else:
            logger.error("Guard Type was not known for {}.".format(guard_type))

        return IDSystemStats(sec, adm, tec, sci)