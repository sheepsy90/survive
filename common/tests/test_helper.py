# -*- coding:utf-8 -*-
import unittest

from common.helper import determine_package_length


class TestHelper(unittest.TestCase):

    def test_determine_package_length(self):

        a = chr(0x5)
        b = chr(0xf)
        e = a+b

        result = determine_package_length(e)

        r = 0x5f
        self.assertEqual(int(r), result)