# -*- coding:utf-8 -*-


# TODO Start the necessary services
# Or make a readme about how to do that
import unittest
from server.xmlrpc_services.crafting.CraftingServiceClient import CraftingServiceClient


class ServiceIntegrationTest(unittest.TestCase):

    def test_crafting_for_tutorial_works(self):
        csc = CraftingServiceClient()

        result = csc.process_crafting_request("11;11;12#11;11;12")

        self.assertEquals(True, result.is_valid_crafting())
        self.assertEquals(False, result.is_crafting_dummy())
        self.assertTrue(1, len(result.get_result()))

        result_element = result.get_result()[0]

        item_template, amount = result_element

        self.assertEqual(1, amount)
        self.assertTrue(13, item_template.type_id)
