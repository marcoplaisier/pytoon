from behave import *
from pytoon.pytoon import Connection

@given('we connect to the master brick')
def step_impl(context):
    brick_conn = Connection()
    context.connected = brick_conn.connect()

@then('we are connected')
def step_impl(context):
    assert context.connected