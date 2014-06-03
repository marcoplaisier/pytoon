#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from flask import Flask, app
from pytoon.connection import BrickConnection


app = Flask(__name__)


class PyToon(object):
    def main(self):
        host = "192.168.178.35"
        port = 4223
        BrickConnection(host, port)

@app.route('/')
def index():
    return '<h1>Test PyToon</h1>'

if __name__ == '__main__':
    PyToon().main()
    app.run(debug=True)
    input()