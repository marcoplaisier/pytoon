from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)


class Electricity(db.Model):
    timestamp = db.Column(db.DateTime, primary_key=True)

    def __repr__(self):
        return '<Timestamp {}>'.format(self.timestamp)