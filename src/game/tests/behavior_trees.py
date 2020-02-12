#!/usr/bin/env python3

import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))


from ai.behavior_tree import *

def test_fun_failure(dt):
    print("test 1 -> return Failure.")
    return NodeTree.FAILURE

def test_fun_success(dt):
    print("test 1 -> return Success.")
    return NodeTree.SUCCESS


root_node = Sequence()

first_selector = Selector()
second_selector = Selector()

leaf_1 = Leaf(test_fun_failure)
leaf_2 = Leaf(test_fun_success)

leaf_3 = Leaf(test_fun_failure)
leaf_4 = Leaf(test_fun_success)


first_selector.append_node(leaf_1)
first_selector.append_node(leaf_2)

second_selector.append_node(leaf_3)
second_selector.append_node(leaf_4)

root_node.append_node(first_selector)
root_node.append_node(second_selector)



root_node.tick(42)