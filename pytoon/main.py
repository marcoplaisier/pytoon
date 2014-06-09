#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from pytoon.connection import BrickConnection
from pytoon.models import db, app, Electricity


@app.route('/')
def index():
    timestamps = Electricity.query.all()
    data = '<table><tbody>'
    for t in timestamps:
        data = data + '<tr><td>{}</td></tr>'.format(t.timestamp)
    data = data + '</tbody></table>'
    return data


class PyToon(object):
    def __init__(self, database):
        host = "192.168.178.35"
        port = 4223
        BrickConnection(host, port, database)

if __name__ == '__main__':
    db.create_all(app=app)
    pt = PyToon(db)

    app.run(debug=True, use_reloader=False)
