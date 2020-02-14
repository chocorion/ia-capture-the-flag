import sys
import os

import unittest

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from ai.behavior_tree import *

TEST_FLAG = False

def test_fun_failure(dt):
    global TEST_FLAG
    TEST_FLAG = False
    return NodeTree.FAILURE

def test_fun_success(dt):
    global TEST_FLAG
    TEST_FLAG = True
    return NodeTree.SUCCESS

class TestBehaviorTree(unittest.TestCase):
    def test_selector_success(self):
        global TEST_FLAG
        TEST_FLAG = False

        root_node = Sequence()

        selector = Selector()

        selector.append_node(Leaf(test_fun_success))
        selector.append_node(Leaf(test_fun_failure))

        root_node.append_node(selector)

        root_node.tick(42)

        self.assertTrue(TEST_FLAG)

    def test_selector_failure(self):
        global TEST_FLAG
        TEST_FLAG = False

        root_node = Sequence()

        selector = Selector()

        selector.append_node(Leaf(test_fun_failure))
        selector.append_node(Leaf(test_fun_success))

        root_node.append_node(selector)

        root_node.tick(42)

        self.assertTrue(TEST_FLAG)