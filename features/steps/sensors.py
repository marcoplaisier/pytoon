from behave import given, when, then
from mock import patch, call
from tinkerforge.ip_connection import IPConnection
<<<<<<< HEAD

@given('we connect to the master brick')
def step_impl(context):
    pass

@then('we are connected')
def step_impl(context):
    pass
=======
from pytoon.main import Electricity, db

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

@when('we have an {sensor_type} sensor')
def step_impl(context, sensor_type):
    if sensor_type == 'electricity':
        context.brick_conn.cb_enumerate('3', None, None, None, None, device_identifier=21,
                                        enumeration_type=IPConnection.ENUMERATION_TYPE_CONNECTED)
        assert (context.brick_conn.ambient is not None )

@then('we can measure {sensor_type}')
def step_impl(context, sensor_type):
    if sensor_type == 'electricity':
        context.brick_conn.cb_ambient()

@then('we store the {sensor_type} measurements in the database')
def step_impl(context, sensor_type):
    result = Electricity.query.all()
    assert result is not None
>>>>>>> electricity
