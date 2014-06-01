#!/usr/bin/env python
# -*- coding: utf-8 -*-  

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_hall_effect import HallEffect
from tinkerforge.bricklet_ambient_light import AmbientLight
from tinkerforge.bricklet_line import Line
from datetime import datetime


class BrickConnection(object):
    def __init__(self, host, port):
        self.hall = None
        self.ambient = None
        self.line = None

        # Create IP Connection
        self.connection = IPConnection()

        # Register IP Connection callbacks
        self.connection.register_callback(IPConnection.CALLBACK_ENUMERATE, self.cb_enumerate)
        self.connection.register_callback(IPConnection.CALLBACK_CONNECTED, self.cb_connected)

        # Connect to brick, will trigger cb_connected
        self.connection.connect(host, port)
        self.connection.enumerate()

    def cb_hall(self, *args, **kwargs):
        print('{} - 0,01m3 gas'. format(datetime.now()))

    def cb_ambient(self, *args, **kwargs):
        print('{} - 1 Wh'.format(datetime.now()))

    def cb_line(self, *args, **kwargs):
        state = self.line.get_reflectivity_callback_threshold()
        print(state)
        if state[0] == Line.THRESHOLD_OPTION_SMALLER:
            print('{} - 0.0001m3'.format(datetime.now()))
            self.line.set_reflectivity_callback_threshold('>', 3900, 0)
        elif state[0] == Line.THRESHOLD_OPTION_GREATER:
            self.line.set_reflectivity_callback_threshold('<', 3880, 0)

    def create_hall_object(self, uid):
        # Create hall device object
        self.hall = HallEffect(uid, self.connection)
        self.hall.register_callback(self.hall.CALLBACK_EDGE_COUNT, self.cb_hall)
        self.hall.set_edge_count_callback_period(100)

    def create_ambient_light_object(self, uid):
        # Create ambient light object
        self.ambient = AmbientLight(uid, self.connection)
        self.ambient.register_callback(self.ambient.CALLBACK_ILLUMINANCE_REACHED, self.cb_ambient)
        self.ambient.set_illuminance_callback_threshold('>', 0, 10)
        self.ambient.set_analog_value_callback_period(400)

    def create_line_object(self, uid):
        # Create line object
        self.line = Line(uid, self.connection)
        self.line.register_callback(self.line.CALLBACK_REFLECTIVITY_REACHED, self.cb_line)
        if self.line.get_reflectivity() > 3890:
            self.line.set_reflectivity_callback_threshold('<', 3880, 0)
        else:
            self.line.set_reflectivity_callback_threshold('>', 3900, 0)
        self.line.set_reflectivity_callback_period(100)

    @staticmethod
    def device_connected(enumeration_type):
        return enumeration_type == IPConnection.ENUMERATION_TYPE_CONNECTED or \
               enumeration_type == IPConnection.ENUMERATION_TYPE_AVAILABLE

    def cb_enumerate(self, uid, connected_uid, position, hardware_version, firmware_version, device_identifier,
                     enumeration_type):
        """
        Callback handles device connections and configures possibly lost configuration of line, hall and reflectivity
        callbacks

        """
        if self.device_connected(enumeration_type):
            if device_identifier == HallEffect.DEVICE_IDENTIFIER:
                self.create_hall_object(uid)
            if device_identifier == AmbientLight.DEVICE_IDENTIFIER:
                self.create_ambient_light_object(uid)
            if device_identifier == Line.DEVICE_IDENTIFIER:
                self.create_line_object(uid)

    def cb_connected(self, connected_reason):
        """
        Callback handles reconnection of IP Connection
        
        Enumerate devices again. If we reconnected, the Brick may have been offline and the configuration may be lost. 
        In this case we don't care for the reason of the connection
        """
        self.connection.enumerate()


if __name__ == "__main__":
    host = "192.168.178.35"
    port = 4223
    BrickConnection(host, port)
    input('Press key to exit\n')