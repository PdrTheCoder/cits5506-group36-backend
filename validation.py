from typing import Optional

from pydantic import BaseModel, validator

from model import Device, db


def device_id_exists(device_id):
    device = db.session.query(Device).filter(Device.id == device_id).first()
    return device is not None


class DeviceCreate(BaseModel):
    name: str
    distance: Optional[float] = None
    empty_distance: Optional[float] = None
    threshold: float
    desc: Optional[str] = None


class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    distance: Optional[float] = None
    empty_distance: Optional[float] = None
    threshold: Optional[float] = None
    desc: Optional[str] = None


class RecordCreate(BaseModel):
    device_id: int
    distance: float

    @validator("device_id")
    def validate_device_id(cls, device_id):
        if not device_id_exists(device_id):
            raise ValueError("Device ID not found in the database")
        return device_id


class RecordUpdate(BaseModel):
    device_id: Optional[int] = None
    distance: Optional[float] = None

    @validator("device_id", always=True)
    def validate_device_id(cls, device_id, values):
        if device_id is not None and not device_id_exists(device_id):
            raise ValueError("Device ID not found in the database")
        return device_id
