#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from pytoon.connection import BrickConnection


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/app.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)


@app.route('/')
def index():
    timestamps = Electricity.query.all()
    return render_template('index.html', data=timestamps)


class PyToon(object):
    def __init__(self, database):
        host = "192.168.178.35"
        port = 4223
        BrickConnection(host, port, database)


class Electricity(db.Model):
    timestamp = db.Column(db.DateTime, primary_key=True)

    def __init__(self, timestamp):
        self.timestamp = timestamp

    def __repr__(self):
        return '{}'.format(self.timestamp)

db.create_all()

if __name__ == '__main__':
    pt = PyToon(db)

    app.run(debug=True, use_reloader=False)
