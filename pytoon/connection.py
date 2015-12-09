# !/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_hall_effect import HallEffect
from tinkerforge.bricklet_ambient_light import AmbientLight
from tinkerforge.bricklet_line import Line


class BrickConnection(object):
    def __init__(self, host, port, database):
        self.hall = None
        self.ambient = None
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

    def cb_ambient(self, *args, **kwargs):
        """Callback for the ambient light sensor.

        When the connected ambient light sensor detects an increase in the luminance, this callback is called. This
        results in the timestamp of this call being written into the database for later processing.
        """
        print("Ambient")
        print(args)
        print(kwargs)

    def create_ambient_light_object(self, uid):
        """Create ambient light object which is used to measure electricity

        My electricity meter uses light flashes to indicate that one Wh is delivered by the utility company. These
        flashes are not easily countable. There are several problems:
        1. The flash is short in duration but not infinitely short,
           If the emitted light flash were infinitely short in duration, then we could determine exactly at which moment
           it occurs and when the next one occurs. Unfortunately, the shape of the flash is as follows. The luminance
           rises very rapidly and then dies down rapidly. So, the flash takes some time (approximately 100 milliseconds)
           to occur. If we naively set a callback for every value other than 0, we would get several measurements for
           one flash.
        2. Flashes are measured having different intensities,
           I'm not sure why this happens, but the bricklet sometimes reports different values for each flash. We cannot
           assume that each flash results in roughly the same intensity.
        3. The time interval between flashes may vary, realistically, between 1 second and 30 seconds or even more.
           These intervals are highly variable, which means that we cannot just take measurements at certain intervals.
        4. Someone may open the closet where the electricity meter is located, inadvertently increasing the light
           intensity. This is still an unsolved problem.

        The solution is to set the debounce period to approximately 400 milliseconds, long enough for the light
        intensity to return to zero after a flash, but short enough to be ready for the next light flash.

        :param uid: the unique identifier for the ambient light sensor
        """
        self.ambient = AmbientLight(uid, self.connection)
        self.ambient.register_callback(self.ambient.CALLBACK_ILLUMINANCE_REACHED, self.cb_ambient)
        self.ambient.set_illuminance_callback_threshold('>', 0, 10)
        self.ambient.set_analog_value_callback_period(400)
        self.ambient.measured_amount = 0

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
        Callback handles device connections and configures possibly lost configuration of line, hall and reflectivity
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
            if device_identifier == AmbientLight.DEVICE_IDENTIFIER:
                self.create_ambient_light_object(uid)

    def cb_connected(self, connected_reason):
        """
        Callback handles reconnection of IP Connection
        
        Enumerate devices again. If we reconnected, the Brick may have been offline and the configuration may be lost. 
        In this case we don't care for the reason of the connection
        :param connected_reason:
        """
        self.connection.enumerate()


if __name__ == "__main__":
    host = "localhost"
    port = 4223
    BrickConnection(host, port)
    input('Press key to exit\n')