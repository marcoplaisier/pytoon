# !/usr/bin/env python
# -*- coding: utf-8 -*-
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_hall_effect import HallEffect
from tinkerforge.bricklet_line import Line
import statsd


class BrickConnection(object):
    ELECTRICITY_BOTTOM_THRESHOLD = 1800
    ELECTRICITY_TOP_THRESHOLD = 1860
    WATER_BOTTOM_THRESHOLD = 3845
    WATER_TOP_THRESHOLD = 3880

    def __init__(self, host, port):
        self.gas_sensor = None
        self.water_sensor = None
        self.electricity_sensor = None
        self.electricity_stat = statsd.Counter('pytoon.water')
        self.gas_stat = statsd.Counter('pytoon.gas')
        self.water_stat = statsd.Counter('pytoon.water')

        # Create IP Connection
        self.connection = IPConnection()

        # Register IP Connection callbacks
        self.connection.register_callback(IPConnection.CALLBACK_ENUMERATE, self.cb_enumerate)
        self.connection.register_callback(IPConnection.CALLBACK_CONNECTED, self.cb_connected)

        # Connect to brick, will trigger cb_connected
        self.connection.connect(host, port)
        self.connection.enumerate()

    def cb_gas(self, *args, **kwargs):
        result = self.gas_stat.increment()
        if not result:
            raise ConnectionError('Cannot reach statsd server')

    def cb_electricity(self, *args, **kwargs):
        if self.electricity_sensor.get_reflectivity_callback_threshold().option == '<':
            self.electricity_sensor.set_reflectivity_callback_threshold('>', self.ELECTRICITY_TOP_THRESHOLD, 0)
        else:
            self.electricity_sensor.set_reflectivity_callback_threshold('<', self.ELECTRICITY_BOTTOM_THRESHOLD, 0)
            result = self.electricity_stat.increment()
            if not result:
                raise ConnectionError('Cannot reach statsd server')

    def cb_water(self, *args, **kwargs):
        if self.water_sensor.get_reflectivity_callback_threshold().option == '<':
            self.water_sensor.set_reflectivity_callback_threshold('>', self.WATER_TOP_THRESHOLD, 0)
        else:
            self.water_sensor.set_reflectivity_callback_threshold('<', self.WATER_BOTTOM_THRESHOLD, 0)
            result = self.water_stat.increment()
            if not result:
                raise ConnectionError('Cannot reach statsd server')

    def create_gas_sensor(self, *args, **kwargs):
        # Create hall device object
        self.gas_sensor = HallEffect(args[0], self.connection)
        self.gas_sensor.register_callback(self.gas_sensor.CALLBACK_EDGE_COUNT, self.cb_gas)
        self.gas_sensor.set_edge_count_callback_period(50)

    def create_water_sensor(self, *args, **kwargs):
        self.water_sensor = Line(args[0], self.connection)
        self.water_sensor.register_callback(self.water_sensor.CALLBACK_REFLECTIVITY_REACHED, self.cb_water)
        self.water_sensor.set_reflectivity_callback_threshold('<', self.WATER_BOTTOM_THRESHOLD, 0)

    def create_electricity_sensor(self, *args, **kwargs):
        # Create line object
        self.electricity_sensor = Line(args[0], self.connection)
        self.electricity_sensor.register_callback(self.line.CALLBACK_REFLECTIVITY_REACHED, self.cb_electricity)
        self.electricity_sensor.set_reflectivity_callback_threshold('<', self.ELECTRICITY_BOTTOM_THRESHOLD, 0)

    @staticmethod
    def is_device_connected(enumeration_type):
        """Check whether new devices become connected or available

        Returns True is a devices is connected to the master brick or becomes available

        :param enumeration_type: the type of connection event, either ENUMERATION_TYPE_CONNECTED,
        ENUMERATION_TYPE_AVAILABLE, or ENUMERATION_TYPE_DISCONNECTED
        :return: boolean indicating whether or not the device is connected
        """
        return enumeration_type == IPConnection.ENUMERATION_TYPE_CONNECTED or \
               enumeration_type == IPConnection.ENUMERATION_TYPE_AVAILABLE

    def cb_enumerate(self, uid, connected_uid, position, hardware_version, firmware_version, device_identifier,
                     enumeration_type):
        """
        Callback handles device connections and configures possibly lost configuration of line and hall callbacks
    
        :param uid: the unique identifier for the bricklet
        :param connected_uid:
        :param position: 
        :param hardware_version: 
        :param firmware_version: 
        :param device_identifier: 
        :param enumeration_type: 
        """
        if self.is_device_connected(enumeration_type):
            if device_identifier == HallEffect.DEVICE_IDENTIFIER:
                self.create_gas_sensor(uid, connected_uid, position, hardware_version, firmware_version,
                                       device_identifier, enumeration_type)
            if device_identifier == Line.DEVICE_IDENTIFIER:
                if position == 'A':
                    self.create_water_sensor(uid, connected_uid, position, hardware_version, firmware_version,
                                             device_identifier, enumeration_type)
                elif position == 'B':
                    self.create_electricity_sensor(uid, connected_uid, position, hardware_version, firmware_version,
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
    host = "192.168.178.42"
    port = 4223
    BrickConnection(host, port)
    input('Press key to exit\n')