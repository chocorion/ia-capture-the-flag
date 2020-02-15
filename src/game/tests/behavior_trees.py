import sys
import os

import unittest

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from ai.behavior_tree import *

DEFAULT_TICK = 100

# Global variable to test effects of functions in leaf
# Warning -> tests can't currently be launched in parallel
TEST_FLAG  = False
TEST_COUNT = 0
TEST_VALUE = 0


# Test function to put in leaf

def test_fun_failure(dt):
    global TEST_FLAG
    TEST_FLAG = False

    return NodeTree.FAILURE


def test_fun_success(dt):
    global TEST_FLAG
    TEST_FLAG = True
    
    return NodeTree.SUCCESS

def increment_count_success(dt):
    global TEST_COUNT

    TEST_COUNT += 1

    return NodeTree.SUCCESS

def set_value_to_one(dt):
    global TEST_VALUE

    TEST_VALUE = 1

class TestBehaviorTree(unittest.TestCase):
    def test_selector_success(self):
        global TEST_FLAG
        TEST_FLAG = False

        root_node = Sequence()

        selector = Selector()

        selector.append_node(Leaf(test_fun_success))
        selector.append_node(Leaf(test_fun_failure))

        root_node.append_node(selector)

        root_node.tick(DEFAULT_TICK)

        self.assertTrue(TEST_FLAG)

    def test_selector_failure(self):
        global TEST_FLAG
        TEST_FLAG = False

        root_node = Sequence()

        selector = Selector()

        selector.append_node(Leaf(test_fun_failure))
        selector.append_node(Leaf(test_fun_success))

        root_node.append_node(selector)

        root_node.tick(DEFAULT_TICK)

        self.assertTrue(TEST_FLAG)

    
    def test_repeater(self):
        global TEST_COUNT

        TEST_COUNT = 0

        root_node = Repeater(42)
        root_node.append_node(Leaf(increment_count_success))

        status = root_node.tick(DEFAULT_TICK)

        self.assertFalse(status == NodeTree.RUNNING)
        self.assertFalse(status == NodeTree.FAILURE)

        self.assertTrue(TEST_COUNT == 42)
        
    
    def test_NodeTreeSingleChild(self):
        single_childe = Repeater(42)

        leaf = Leaf(test_fun_success)

        single_childe.append_node(leaf)

        with self.assertRaises(Exception):
            single_childe.append_node(leaf)

        with self.assertRaises(Exception):
            single_childe.insert_node(leaf)
        

    def test_inverter_on_failure(self):
        root_node = Inverter()
        leaf = Leaf(test_fun_failure)

        root_node.append_node(leaf)

        status = root_node.tick(DEFAULT_TICK)

        self.assertTrue(status == NodeTree.SUCCESS)


    def test_inverter_on_success(self):
        root_node = Inverter()
        leaf = Leaf(test_fun_success)

        root_node.append_node(leaf)

        status = root_node.tick(DEFAULT_TICK)

        self.assertTrue(status == NodeTree.FAILURE)


    def test_succeeder_on_failure(self):
        root_node = Succeeder()
        leaf = Leaf(test_fun_failure)

        root_node.append_node(leaf)

        status = root_node.tick(DEFAULT_TICK)

        self.assertTrue(status == NodeTree.SUCCESS)


    def test_succeeder_on_success(self):
        root_node = Succeeder()
        leaf = Leaf(test_fun_success)

        root_node.append_node(leaf)

        status = root_node.tick(DEFAULT_TICK)

        self.assertTrue(status == NodeTree.SUCCESS)


    def test_condition_on_true(self):
        global TEST_VALUE
        TEST_VALUE = 0

        def fun():
            return True

        root_node = Condition(fun)
        root_node.append_node(Leaf(set_value_to_one))

        root_node.tick(DEFAULT_TICK)

        self.assertTrue(TEST_VALUE == 1)


    def test_condition_on_false(self):
        global TEST_VALUE
        TEST_VALUE = 0

        def fun():
            return False

        root_node = Condition(fun)
        root_node.append_node(Leaf(set_value_to_one))

        root_node.tick(DEFAULT_TICK)

        self.assertTrue(TEST_VALUE != 1)