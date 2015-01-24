#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pytoon
----------------------------------

Tests for `pytoon` module.
"""

import unittest
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from mock import patch, Mock
from pytoon.main import PyToon


@patch('pytoon.main.BrickConnection')
class TestPytoon(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/app.db'
        app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
        self.db = SQLAlchemy(app)

    def test_main_loop(self, mock_class):
        PyToon(self.db)

if __name__ == '__main__':
    unittest.main()