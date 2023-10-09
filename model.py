from email.utils import parsedate_to_datetime
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Device(db.Model):
    """default device model"""

    __tablename__ = "device"
    id = mapped_column(db.Integer, primary_key=True)
    name = mapped_column(db.String(30), unique=True, nullable=False)
    distance = mapped_column(db.Float)
    empty_distance = mapped_column(db.Float)
    threshold = mapped_column(db.Float, nullable=False)
    desc = mapped_column(db.Text)
    created_at = mapped_column(
        db.DateTime(), nullable=False, default=datetime.datetime.utcnow()
    )
    updated_at = mapped_column(db.DateTime())

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "distance": self.distance,
            "empty_distance": self.empty_distance,
            "threshold": self.threshold,
            "desc": self.desc,
            "created_at": self.created_at.isoformat(sep=' ', timespec='seconds'),
            "updated_at": self.updated_at and self.updated_at.isoformat(sep=' ', timespec='seconds')
        }


class Record(db.Model):
    """default model for records"""

    __tablename__ = "record"
    id = mapped_column(db.Integer, primary_key=True)
    device_id = mapped_column(
        db.Integer, db.ForeignKey("device.id", ondelete="CASCADE")
    )
    distance = mapped_column(db.Float, nullable=False)
    created_at = mapped_column(
        db.DateTime(), nullable=False, default=datetime.datetime.utcnow()
    )

    def as_dict(self):
        return {
            "id": self.id,
            "device_id": self.device_id,
            "distance": self.distance,
            "created_at": self.created_at.isoformat(sep=' ', timespec='seconds'),
        }
