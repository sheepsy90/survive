# -*- coding:utf-8 -*-
import unittest
from server.xmlrpc_services.crafting.CraftingPersistence import CraftingPersistence


class TestCraftingPersistence(unittest.TestCase):

    def test_initialization(self):
        cp = CraftingPersistence(":memory:")

        cp.print_all_item_types()

        item_template = cp.load_item_type_from_database(15)

        self.assertEqual(15, item_template.type_id)
        self.assertEqual("item/drink/bottles/water_bottle", item_template.path)
        self.assertEqual("Water Bottle", item_template.name)
        self.assertEqual(u'wearable,hand,consumable,consumes_as_drink', item_template.type_tags)
        self.assertEqual(3, item_template.initial_uses)
        self.assertEqual((1, 2), item_template.shape)

        self.assertFalse(cp.save_item_template(4, "SampleName", (3, 4), 0))
        self.assertTrue(cp.save_item_template(10000, "SampleName", (3, 4), 0))

        cp.print_all_item_types()

        item_templates = cp.get_item_types_by_drop_path_and_level("item/medical/basics", 1)

        self.assertEqual(2, len(item_templates))

        print item_templates