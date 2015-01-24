#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pytoon
----------------------------------

Tests for `pytoon` module.
"""

import unittest
from mock import patch, Mock
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_hall_effect import HallEffect
from tinkerforge.bricklet_ambient_light import AmbientLight
from tinkerforge.bricklet_line import Line
from pytoon.connection import BrickConnection
from pytoon.main import db


class TestConnection(unittest.TestCase):
    def setUp(self):
        self.patch_ip_connection = patch('pytoon.connection.IPConnection')
        self.patch_ip_connection.start()
        host = "192.168.178.35"
        port = 4223
        self.bc = BrickConnection(host, port, db)

    def test_cb_connected(self):
        self.bc.connection.reset_mock()
        self.bc.cb_connected('testing')
        self.bc.connection.enumerate.assert_called_once_with()

    def test_cb_enumerate_hall(self):
        self.assertIsNone(self.bc.hall)
        self.patch_ip_connection.stop()
        self.bc.cb_enumerate('1', None, None, None, None, device_identifier=240,
                             enumeration_type=IPConnection.ENUMERATION_TYPE_CONNECTED)
        self.assertIsNotNone(self.bc.hall)
        self.patch_ip_connection.start()

    def test_cb_enumerate_line(self):
        self.assertIsNone(self.bc.line)
        self.patch_ip_connection.stop()
        self.bc.cb_enumerate('2', None, None, None, None, device_identifier=241,
                             enumeration_type=IPConnection.ENUMERATION_TYPE_CONNECTED)
        self.assertIsNotNone(self.bc.line)
        self.patch_ip_connection.start()

    def tearDown(self):
        self.patch_ip_connection.stop()

if __name__ == '__main__':
    unittest.main()