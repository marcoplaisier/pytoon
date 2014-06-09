#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from multiprocessing import Pipe
from flask import Flask, app
import time
from pytoon.connection import BrickConnection
from flask.ext.sqlalchemy import SQLAlchemy


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

@app.route('/')
def index():
    return '<h1>Test PyToon</h1>'


class Timestamp(db.Model):
    __tablename__ = 'electricity'
    timestamp = db.Column(db.DateTime, primary_key=True)


class PyToon(object):
    def __init__(self):
        input_p, self.output_p = Pipe()
        host = "192.168.178.35"
        port = 4223
        BrickConnection(host, port, input_p)

    def main_loop(self):
        while True:
            time.sleep(0.5)
            if self.output_p.poll(0):
                db.session.add(self.output_p.recv())

if __name__ == '__main__':
    pt = PyToon()

    app.run(debug=True, use_reloader=False)