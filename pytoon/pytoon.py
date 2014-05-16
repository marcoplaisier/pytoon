#!/usr/bin/env python
# -*- coding: utf-8 -*-


from tinkerforge.ip_connection import IPConnection


class Connection(object):
    HOST = "192.168.178.35"
    PORT = 4223

    def __init__(self):
        self.ipcon = IPConnection()

    def connect(self):
        self.ipcon.connect(host=self.HOST, port=self.PORT)
        return self.ipcon.get_connection_state()