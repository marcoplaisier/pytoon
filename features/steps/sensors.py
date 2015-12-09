from behave import given, when, then
from mock import patch, call
from tinkerforge.bricklet_ambient_light import AmbientLight
from tinkerforge.bricklet_hall_effect import HallEffect
from tinkerforge.ip_connection import IPConnection
from pytoon.main import db, Electricity, Gas
from pytoon.connection import BrickConnection


@given('we connect to the master brick')
@patch('pytoon.connection.IPConnection')
def step_impl(context, mock_class):
    host = None
    port = None
    context.brick_conn = BrickConnection(host, port, db)

@then('we are connected')
def step_impl(context):
    calls = [call(), call()]
    context.brick_conn.connection.register_callback.has_calls(calls)

@when('we have a {sensor_type} sensor')
def step_impl(context, sensor_type):
    if sensor_type == 'electricity':
        context.brick_conn.cb_enumerate('3', None, None, None, None, device_identifier=AmbientLight.DEVICE_IDENTIFIER,
                                        enumeration_type=IPConnection.ENUMERATION_TYPE_CONNECTED)
        assert (context.brick_conn.ambient is not None)
    elif sensor_type == 'gas':
        context.brick_conn.cb_enumerate('2', None, None, None, None, device_identifier=HallEffect.DEVICE_IDENTIFIER,
                                        enumeration_type=IPConnection.ENUMERATION_TYPE_CONNECTED)
    else:
        assert False

@then('we can measure {sensor_type}')
def step_impl(context, sensor_type):
    if sensor_type == 'electricity':
        context.brick_conn.cb_ambient()
    elif sensor_type == 'gas':
        context.brick_conn.cb_hall()
    else:
        assert False