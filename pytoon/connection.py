# !/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_hall_effect import HallEffect
from tinkerforge.bricklet_line import Line
from pytoon.conf import *


class BrickConnection(object):
    def __init__(self, host, port, database):
        self.hall = None
        self.line = None
        self.database = database

        # Create IP Connection
        self.connection = IPConnection()

        # Register IP Connection callbacks
        self.connection.register_callback(IPConnection.CALLBACK_ENUMERATE, self.cb_enumerate)
        self.connection.register_callback(IPConnection.CALLBACK_CONNECTED, self.cb_connected)

        # Connect to brick, will trigger cb_connected
        self.connection.connect(host, port)
        self.connection.enumerate()

    def cb_hall(self, *args, **kwargs):
        from pytoon.main import Gas
        if args[1]:
            gas_timestamp = Gas(timestamp=datetime.now())
            print('Gas: {}'.format(gas_timestamp))
            print(args, kwargs)
            self.database.session.add(gas_timestamp)
            self.database.session.commit()

    def cb_line(self, *args, **kwargs):
        setting = self.line.get_reflectivity_callback_threshold()
        if setting.option == '<':
            self.line.set_reflectivity_callback_threshold('>', ELECTRICITY_REFLECTIVITY_THRESHOLD, 0)
        elif setting.option == '>':
            self.line.set_reflectivity_callback_threshold('<', ELECTRICITY_REFLECTIVITY_THRESHOLD, 0)
            from pytoon.main import Electricity
            print(args, kwargs)
            electricity_timestamp = Electricity(timestamp=datetime.now())
            print('Electricity: {}'.format(electricity_timestamp))
            self.database.session.add(electricity_timestamp)
            self.database.session.commit()
        else:
            raise NotImplemented("This callback option is not implemented")

    def create_hall_object(self, *args, **kwargs):
        # Create hall device object
        self.hall = HallEffect(args[0], self.connection)
        self.hall.register_callback(self.hall.CALLBACK_EDGE_COUNT, self.cb_hall)
        self.hall.set_edge_count_callback_period(50)

    def create_line_object(self, *args, **kwargs):
        # Create line object
        self.line = Line(args[0], self.connection)
        self.line.register_callback(self.line.CALLBACK_REFLECTIVITY_REACHED, self.cb_line)
        self.line.set_reflectivity_callback_threshold('<', ELECTRICITY_REFLECTIVITY_THRESHOLD, 0)

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
        Callback handles device connections and configures possibly lost configuration of hall and reflectivity
        callbacks
    
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
                self.create_hall_object(uid, connected_uid, position, hardware_version, firmware_version,
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
    from pytoon.main import db

    host = "192.168.178.42"
    port = 4223
    BrickConnection(host, port, db)
    input('Press key to exit\n')