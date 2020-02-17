import sys
import os

import unittest

PACKAGE_PARENT = '../game'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from model.DictBuilder import DictBuilder

def fill_builder(builder):
    for i in range(5):
        builder.add_bot()

        builder.add_life(42)
        builder.add_flag(0)
        builder.add_cooldown(0)

class TestDictBuilder(unittest.TestCase):
    def test_empty_arg(self):
        argBuilder = DictBuilder()

        argBuilder.begin_argument()

        with self.assertRaises(Exception):
            argBuilder.end_argument()


    # TODO: replace 5 by config value
    def test_add_more_than_five(self):
        dictBuilder = DictBuilder()

        dictBuilder.begin_argument()

        fill_builder(dictBuilder)

        with self.assertRaises(Exception):
            dictBuilder.add_bot()


    def test_get_empty_result(self):
        dictBuilder = DictBuilder()
        dictBuilder.begin_argument()

        with self.assertRaises(Exception):
            dictBuilder.get_result()
            

    def test_finish_incomplete_bot(self):
        dictBuilder = DictBuilder()
        dictBuilder.begin_argument()

        dictBuilder.add_bot()
        dictBuilder.add_life(42)

        with self.assertRaises(Exception):
            dictBuilder.add_bot()

    
    def test_valid_construction(self):
        dictBuilder = DictBuilder()
        
        dictBuilder.begin_argument()
        fill_builder(dictBuilder)
        dictBuilder.end_argument()

        result = dictBuilder.get_result()

        for i in range(1, 6):
            if i not in result.keys():
                self.fail("Bot number {} not in result keys !".format(i))

            for parameter in ["life", "flag", "cooldown"]:
                if parameter not in result[i].keys():
                    self.fail("Parameter {} wasn't set in bot number {}.".format(parameter, i))

        