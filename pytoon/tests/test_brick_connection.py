#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pytoon
----------------------------------

Tests for `pytoon` module.
"""

import unittest
from mock import patch, Mock
from pytoon.connection import BrickConnection


@patch('pytoon.connection.IPConnection')
class TestConnection(unittest.TestCase):
    def test_main_loop(self, mock_class):
        host = "192.168.178.35"
        port = 4223
        bc = BrickConnection(host, port)

if __name__ == '__main__':
    unittest.main()