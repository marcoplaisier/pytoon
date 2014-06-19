#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pytoon
----------------------------------

Tests for `pytoon` module.
"""

import unittest
from mock import patch, Mock
from pytoon.main import PyToon


@patch('pytoon.main.BrickConnection')
class TestPytoon(unittest.TestCase):
    def test_main_loop(self, mock_class):
        PyToon().main()

if __name__ == '__main__':
    unittest.main()