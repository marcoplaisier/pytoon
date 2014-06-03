# !/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import sqlite3
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_hall_effect import HallEffect
from tinkerforge.bricklet_ambient_light import AmbientLight
from tinkerforge.bricklet_line import Line


class BrickConnection(object):
    def __init__(self, host, port):
        self.hall = None
        self.ambient = None
        self.line = None

        self.db_conn = sqlite3.connect('app.db')
        c = self.db_conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS electricity (date TEXT, hour INTEGER, minute INTEGER, second INTEGER,
                     microsecond INTEGER)''')
        self.db_conn.commit()
        self.db_conn.close()

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
        """Callback for the ambient light sensor.

        When the connected ambient light sensor detects an increase in the luminance, this callback is called. This
        results in the timestamp of this call being written into the database for later processing.
        """
        print("called")
        db_conn = sqlite3.connect('app.db')
        c = db_conn.cursor()
        dt = datetime.now()

        c.execute('''INSERT INTO electricity VALUES (?, ?, ?, ?, ?)''',
                  (dt.date(), dt.hour, dt.minute, dt.second, dt.microsecond))
        db_conn.commit()
        c.close()

    def cb_line(self, *args, **kwargs):
        pass

    def create_hall_object(self, *args, **kwargs):
        # Create hall device object
        self.hall = HallEffect(args[0], self.connection)
        self.hall.register_callback(self.hall.CALLBACK_EDGE_COUNT, self.cb_hall)
        self.hall.set_edge_count_callback_period(50)

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

    def create_line_object(self, *args, **kwargs):
        # Create line object
        self.line = Line(args[0], self.connection)
        self.line.register_callback(self.line.CALLBACK_REFLECTIVITY_REACHED, self.cb_line)
        self.line.set_reflectivity_callback_threshold('>', 3905, 0)

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
            if device_identifier == HallEffect.DEVICE_IDENTIFIER:
                self.create_hall_object(uid, connected_uid, position, hardware_version, firmware_version,
                                        device_identifier, enumeration_type)
            if device_identifier == AmbientLight.DEVICE_IDENTIFIER:
                self.create_ambient_light_object(uid)
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
    host = "192.168.178.35"
    port = 4223
    BrickConnection(host, port)
    input('Press key to exit\n')