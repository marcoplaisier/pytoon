from behave import *
from pytoon.connection import BrickConnection
from mock import patch, call

@given('we connect to the master brick')
@patch('pytoon.connection.IPConnection')
def step_impl(context, mock_class):
    host = None
    port = None
    context.brick_conn = BrickConnection(host, port)

@then('we are connected')
def step_impl(context):
    calls = [call(), call()]
    context.brick_conn.connection.register_callback.has_calls(calls)