from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://postgres:postgres@airco_db:5432/airco_db"
db = SQLAlchemy(app)


class Status(db.Model):
    name = db.Column(db.VARCHAR, primary_key=True)
    time = db.Column(db.TIMESTAMP, primary_key=True, default=datetime.now())
    target = db.Column(db.INTEGER)
    inside = db.Column(db.INTEGER)
    outside = db.Column(db.INTEGER)
    heat = db.Column(db.INTEGER)
    cool = db.Column(db.INTEGER)
    mode = db.Column(db.VARCHAR)
    power = db.Column(db.INTEGER)
    fan = db.Column(db.VARCHAR)


def insertStatus(status):
    stat = Status(name=status['name'], time=status['time'], target=status['target'], inside=status['inside'],
                  outside=status['outside'], heat=status['heat'], cool=status['cool'], mode=status['mode'],
                  power=status['power'], fan=status['fan'])
    db.session.add(stat)
    db.session.commit()
