#!/usr/bin/python
# -*- coding: utf-8 -*-
from pytoon.main import db


def get_consumption_per_time_unit(consumption_type, time_unit='hour'):
    return db.session.query(consumption_type.timestamp, db.func.count(consumption_type.timestamp)).\
        group_by(db.func.extract(time_unit, consumption_type.timestamp)).\
        all()