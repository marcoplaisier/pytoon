#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pytoon.connection import BrickConnection


class PyToon(object):
    def __init__(self, database):
        host = "localhost"
        port = 4223
        BrickConnection(host, port, database)