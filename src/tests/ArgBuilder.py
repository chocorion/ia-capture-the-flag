import sys
import os

import unittest

PACKAGE_PARENT = '../game'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from model.DictBuilder import DictBuilder

class TestDictBuilder(unittest.TestCase):
    def test_empty_arg(self):
        argBuilder = DictBuilder()

        argBuilder.begin_argument()

        with self.assertRaises(Exception):
            argBuilder.end_argument()
