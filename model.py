import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


class Device(db.Model):
    __tablename__ = "device"
    id = mapped_column(db.Integer, primary_key=True)
    name = mapped_column(db.String(30), unique=True, nullable=False)
    distance = mapped_column(db.Float)
    empty_distance = mapped_column(db.Float)
    threshold = mapped_column(db.Float, nullable=False)
    desc = mapped_column(db.Text)
    created_at = mapped_column(db.DateTime(), nullable=False, default=datetime.datetime.utcnow())
    updated_at = mapped_column(db.DateTime())

    def as_dict(self):
        # TODO ADD MORE ATTRIBUTE TO BELOW
        return {
            "id": self.id
        }


class Record(db.Model):
    __tablename__ = "record"
    id = mapped_column(db.Integer, primary_key=True)
    dId = mapped_column(db.Integer)
    distance = mapped_column(db.Float, nullable=False)
    created_at = mapped_column(db.DateTime(), nullable=False, default=datetime.datetime.utcnow())
