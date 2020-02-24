import sys
import os

import unittest

PACKAGE_PARENT = '../game'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from model.ArgBuilder.DictBuilder import DictBuilder
from service import *
from domain.GameObject.Bot.RegularBot import RegularBot

def fill_builder(builder):
    botId = 0

    for i in range(5):
        builder.addBot(RegularBot(1, 1, 1), botId)
        botId += 1

class TestDictBuilder(unittest.TestCase):

    def __init__(self, methodName):
        super().__init__(methodName)
        Config.Initialize()
        Ruleset.Initialize()


    def test_empty_arg(self):
        argBuilder = DictBuilder()

        argBuilder.beginArgument()

        with self.assertRaises(Exception):
            argBuilder.endArgument()


    # TODO: replace 5 by config value
    def test_add_more_than_five(self):
        dictBuilder = DictBuilder()

        dictBuilder.beginArgument()

        fill_builder(dictBuilder)

        with self.assertRaises(Exception):
            dictBuilder.addBot(RegularBot(1, 0, 0), 0)


    def test_get_empty_result(self):
        dictBuilder = DictBuilder()
        dictBuilder.beginArgument()

        with self.assertRaises(Exception):
            dictBuilder.getResult()
            

    def test_finish_incomplete_bot(self):
        dictBuilder = DictBuilder()
        dictBuilder.beginArgument()

        dictBuilder.addBot(RegularBot(1, 0, 0), 0)

        with self.assertRaises(Exception):
            dictBuilder.endArgument()

    
    def test_valid_construction(self):
        dictBuilder = DictBuilder()
        
        dictBuilder.beginArgument()
        fill_builder(dictBuilder)
        dictBuilder.endArgument()

        result = dictBuilder.getResult()

        for i in range(5):
            if i not in result["bots"].keys():
                self.fail("Bot number {} not in result keys !".format(i))

            for parameter in ["life", "flag", "cooldown"]:
                if parameter not in result["bots"][i].keys():
                    self.fail("Parameter {} wasn't set in bot number {}.".format(parameter, i))

        