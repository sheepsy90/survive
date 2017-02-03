# -*- coding:utf-8 -*-
import unittest

from common.ItemTemplate import ItemTemplate
from common.ItemTemplateTags import ItemTemplateTags
from common.constants.ContainerConstants import ContainerConstants
from server.world_objects.object_components.ContainerComponent import Container
from server.world_objects.object_components.NpcComponent import NpcComponent
from server.xmlrpc_services.items.Item import Item


class TestContainer(unittest.TestCase):

    def assert_sufficient_id_card_works(self, container, category, level0=True, level1=False, level2=False, level3=False):
        self.assertEqual(level0, container.has_sufficient_id_card(category, 0))
        self.assertEqual(level1, container.has_sufficient_id_card(category, 1))
        self.assertEqual(level2, container.has_sufficient_id_card(category, 2))
        self.assertEqual(level3, container.has_sufficient_id_card(category, 3))

    def prepare_container(self, item_template_tags_for_card):
        item_type_id = 1
        shape = (3, 2)
        usages = 0
        item_template_card = ItemTemplate("item_template_card", "", "", item_type_id, shape, usages,
                                          item_template_tags_for_card)
        item_card = Item(item_template_card, 1, usages)
        # Another item type which we use to check for behaviour with other items in list
        zwirn_type = ItemTemplate("Zwirn", "", "", 3, (1, 2), 1, ItemTemplateTags.from_list())
        zwirn = Item(zwirn_type, 2, 1)
        c = Container(True, (6, 6), ContainerConstants.CONTAINER_TYPE_NORMAL)
        c.prepare_content(empty=True)
        self.assertTrue(c.put_item_if_fits(item_card, (0, 0)))
        self.assertTrue(c.put_item_if_fits(zwirn, (3, 0)))
        return c

    def test_id_card_equal_level_is_allowed(self):
        c = self.prepare_container(ItemTemplateTags.from_list(ItemTemplateTags.SECURITY_1,
                                                              ItemTemplateTags.HAND,
                                                              ItemTemplateTags.WEARABLE))

        self.assert_sufficient_id_card_works(c, NpcComponent.GUARD_TYPE_SECURITY, level1=True)
        self.assert_sufficient_id_card_works(c, NpcComponent.GUARD_TYPE_ADMINISTRATION)
        self.assert_sufficient_id_card_works(c, NpcComponent.GUARD_TYPE_SCIENCE)
        self.assert_sufficient_id_card_works(c, NpcComponent.GUARD_TYPE_TECHNICIAN)

    def test_id_card_higher_level_is_allowed(self):
        c = self.prepare_container(ItemTemplateTags.from_list(ItemTemplateTags.SECURITY_2,
                                                              ItemTemplateTags.HAND,
                                                              ItemTemplateTags.WEARABLE))

        self.assert_sufficient_id_card_works(c, NpcComponent.GUARD_TYPE_SECURITY, level1=True, level2=True)
        self.assert_sufficient_id_card_works(c, NpcComponent.GUARD_TYPE_ADMINISTRATION)
        self.assert_sufficient_id_card_works(c, NpcComponent.GUARD_TYPE_SCIENCE)
        self.assert_sufficient_id_card_works(c, NpcComponent.GUARD_TYPE_TECHNICIAN)

    def test_id_card_with_multiple_properties_worked(self):
        c = self.prepare_container(ItemTemplateTags.from_list(ItemTemplateTags.SECURITY_1,
                                                              ItemTemplateTags.TECHNICIAN_1,
                                                              ItemTemplateTags.HAND,
                                                              ItemTemplateTags.WEARABLE))

        self.assert_sufficient_id_card_works(c, NpcComponent.GUARD_TYPE_SECURITY, level1=True)
        self.assert_sufficient_id_card_works(c, NpcComponent.GUARD_TYPE_ADMINISTRATION)
        self.assert_sufficient_id_card_works(c, NpcComponent.GUARD_TYPE_SCIENCE)
        self.assert_sufficient_id_card_works(c, NpcComponent.GUARD_TYPE_TECHNICIAN, level1=True)


    def test_that(self):
        c = Container(True, (3, 3), ContainerConstants.CONTAINER_TYPE_NORMAL)
        c.prepare_content(empty=True)

        needle_type = ItemTemplate("Needle", "", "", 2, (2, 1), 1, ItemTemplateTags.from_list())
        needle = Item(needle_type, 1, 1)
        zwirn_type = ItemTemplate("Zwirn", "", "", 3, (1, 2), 1, ItemTemplateTags.from_list())
        zwirn = Item(zwirn_type, 2, 1)

        self.assertTrue(c.put_item_if_fits(needle, (0, 0)))
        self.assertTrue(c.put_item_if_fits(zwirn, (2, 0)))

        self.assertEqual(c.shape_mapping.tolist(), [[1, 0, 0], [1, 0, 0], [2, 2, 0]])
        self.assertEqual("2;0#2;0#3;3", c.get_representation_for_crafting())

    def test_produces_correct_representation(self):
        c = Container(True, (3, 3), ContainerConstants.CONTAINER_TYPE_NORMAL)
        c.prepare_content(empty=True)

        needle_type = ItemTemplate("Needle", "", "", 1, (3, 1), 1, ItemTemplateTags.from_list())
        zwirn_type = ItemTemplate("Zwirn", "", "", 2, (1, 2), 1, ItemTemplateTags.from_list())
        needle = Item(needle_type, 1, 1)
        zwirn = Item(zwirn_type, 2, 1)

        self.assertTrue(c.put_item_if_fits(needle, (0, 0)))
        self.assertTrue(c.put_item_if_fits(zwirn, (2, 1)))

        result = "1;0;0#1;0;0#1;2;2"

        self.assertEqual(result, c.get_representation_for_crafting())


        self.assertTrue(c.put_item_if_fits(needle, (0, 0)))
        self.assertTrue(c.put_item_if_fits(zwirn, (1, 1)))

        result = "1;0;0#1;2;2#1;0;0"

        self.assertEqual(result, c.get_representation_for_crafting())

        c.remove_item(needle)

        result = "2;2"
        self.assertEqual(result, c.get_representation_for_crafting())