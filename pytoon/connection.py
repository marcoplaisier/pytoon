#!/usr/bin/env python
# -*- coding: utf-8 -*-  

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_hall_effect import HallEffect
from tinkerforge.bricklet_ambient_light import AmbientLight
from tinkerforge.bricklet_line import Line


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
        pass

    def cb_ambient(self, *args, **kwargs):
        pass

    def cb_line(self, *args, **kwargs):
        pass

    def create_hall_object(self, *args, **kwargs):
        # Create hall device object
        self.hall = HallEffect(args[0], self.connection)
        self.hall.register_callback(self.hall.CALLBACK_EDGE_COUNT, self.cb_hall)
        self.hall.set_edge_count_callback_period(50)

    def create_ambient_light_object(self, *args, **kwargs):
        # Create ambient light object
        self.ambient = AmbientLight(args[0], self.connection)
        self.ambient.register_callback(self.ambient.CALLBACK_ILLUMINANCE_REACHED, self.cb_ambient)
        self.ambient.set_illuminance_callback_threshold('>', 0, 10)

    def create_line_object(self, *args, **kwargs):
        # Create line object
        self.line = Line(args[0], self.connection)
        self.line.register_callback(self.line.CALLBACK_REFLECTIVITY_REACHED, self.cb_line)
        self.line.set_reflectivity_callback_threshold('>', 3905, 0)

    @staticmethod
    def device_connected(enumeration_type):
        return enumeration_type == IPConnection.ENUMERATION_TYPE_CONNECTED or \
               enumeration_type == IPConnection.ENUMERATION_TYPE_AVAILABLE

    def cb_enumerate(self, uid, connected_uid, position, hardware_version, firmware_version, device_identifier,
                     enumeration_type):
        """
        Callback handles device connections and configures possibly lost configuration of line, hall and reflectivity
        callbacks
    
        :param uid: 
        :param connected_uid: 
        :param position: 
        :param hardware_version: 
        :param firmware_version: 
        :param device_identifier: 
        :param enumeration_type: 
        """
        if self.device_connected(enumeration_type):
            if device_identifier == HallEffect.DEVICE_IDENTIFIER:
                self.create_hall_object(uid, connected_uid, position, hardware_version, firmware_version,
                                        device_identifier, enumeration_type)
            if device_identifier == AmbientLight.DEVICE_IDENTIFIER:
                self.create_ambient_light_object(uid, connected_uid, position, hardware_version, firmware_version,
                                                 device_identifier, enumeration_type)
            if device_identifier == Line.DEVICE_IDENTIFIER:
                self.create_line_object(uid, connected_uid, position, hardware_version, firmware_version,
                                        device_identifier, enumeration_type)

    def cb_connected(self, connected_reason):
        """
        Callback handles reconnection of IP Connection
        
        Enumerate devices again. If we reconnected, the Brick may have been offline and the configuration may be lost. 
        In this case we don't care for the reason of the connection
        :param connected_reason: 
        """
        self.connection.enumerate()


if __name__ == "__main__":
    BrickConnection()
    input('Press key to exit\n')