from behave import given, when, then
from mock import patch, call
from tinkerforge.ip_connection import IPConnection

@given('we connect to the master brick')
def step_impl(context):
    pass

@then('we are connected')
def step_impl(context):
    pass