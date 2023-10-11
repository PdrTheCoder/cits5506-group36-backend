# using flask_restful
import datetime

from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api, Resource
from model import Device, Record, db
from pydantic import ValidationError
from sqlalchemy import desc
from utils import error_res, ok_res, res
from validation import DeviceCreate, DeviceUpdate, RecordCreate, RecordUpdate

# creating the flask app
app = Flask(__name__)

# cors for all apis
CORS(app)

# configure database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)


# creating an API object
api = Api(app)


class DeviceList(Resource):
    """list devices or create a device"""

    def get(self):
        """list all devices"""
        devices = db.session.query(Device).order_by(Device.name).all()
        data = [device.as_dict() for device in devices]
        return ok_res(data=data)

    def post(self):
        """create a device"""
        data = request.get_json()
        code = -1
        res_data = None

        try:
            device_create = DeviceCreate(**data)
        except ValidationError as e:
            return error_res(f"Invalid input: {str(e)}")

        device = Device(**device_create.model_dump())

        try:
            db.session.add(device)
            db.session.commit()
            res_data = {"id": device.id}
            msg = "Device added."
            code = 0
        except Exception as e:
            db.session.rollback()
            msg = f"Failed to register the device. Reason: {str(e)}"
        finally:
            db.session.close()
        return res(msg=msg, code=code, data=res_data)


class DeviceItem(Resource):
    """get, update, delete a device"""

    def get(self, device_id):
        """get a device by id"""
        device = db.session.get(Device, device_id)
        if device is None:
            return error_res("Device not found")
        return ok_res(data=device.as_dict())

    def patch(self, device_id):
        """update a device by id"""
        data = request.get_json()
        device = db.session.get(Device, device_id)

        code = -1
        res_data = None

        if device is None:
            return error_res("Error: Device not found")
        try:
            device_update = DeviceUpdate(**data)
        except ValidationError as e:
            return error_res(f"Invalid input: {str(e)}")

        try:
            for key, value in device_update.model_dump().items():
                if key == "updated_at":
                    continue
                if value is not None:
                    setattr(device, key, value)
            device.updated_at = datetime.datetime.utcnow()
            db.session.commit()
            res_data = device.as_dict()
            code = 0
            msg = "Device updated."
            return ok_res(msg="Device updated", data=device.as_dict())
        except (KeyError, AttributeError) as e:
            db.session.rollback()
            msg = f"Error: {str(e)}"
        finally:
            db.session.close()
        return res(msg=msg, code=code, data=res_data)

    def delete(self, device_id):
        """delete a device by id"""
        device = db.session.get(Device, device_id)
        if device is None:
            return error_res("Error: Device not found")
        db.session.delete(device)

        res_data = None
        code = -1
        try:
            db.session.commit()
            code = 0
            msg = "Device deleted."
        except Exception as e:
            db.session.rollback()
            msg = f"Error: {str(e)}"
        finally:
            db.session.close()
        return res(msg=msg, code=code, data=res_data)


class RecordList(Resource):
    """List records or create a record"""

    def get(self):
        """get all records"""
        records = db.session.query(Record).all()
        data = [record.as_dict() for record in records]
        return ok_res(data=data)

    def post(self):
        """create a record"""
        data = request.get_json()
        code = -1
        res_data = None

        try:
            record_create = RecordCreate(**data)
        except ValidationError as e:
            return error_res(f"Invalid input: {str(e)}")

        record = Record(**record_create.model_dump())

        try:
            db.session.add(record)
            db.session.commit()
            code = 0
            msg = "Record added."
            res_data = {"id": record.id}
        except Exception as e:
            db.session.rollback()
            msg = f"Failed to register the record. Reason: {str(e)}"
        finally:
            db.session.close()
        return res(msg=msg, code=code, data=res_data)


class RecordItem(Resource):
    """get, update, delete a record"""

    def get(self, record_id):
        """get record by id"""
        record = db.session.get(Record, record_id)
        if record is None:
            return error_res("Record not found")
        return ok_res(data=record.as_dict())

    def patch(self, record_id):
        """update a record by id"""
        data = request.get_json()
        record = db.session.get(Record, record_id)
        res_data = None
        code = -1

        if record is None:
            return error_res("Error: Record not found")

        try:
            record_update = RecordUpdate(**data)
        except ValidationError as e:
            return error_res(f"Invalid input: {str(e)}")

        try:
            for key, value in record_update.model_dump().items():
                if key == "updated_at":
                    continue
                if value is not None:
                    setattr(record, key, value)
            record.updated_at = datetime.datetime.utcnow()
            db.session.commit()
            code = 0
            res_data = record.as_dict()
            msg = "Record updated"
        except (KeyError, AttributeError) as e:
            db.session.rollback()
        finally:
            db.session.close()
        return res(msg, code, data=res_data)


class DeviceRecords(Resource):
    """Get records for a specific device"""

    def get(self, device_id):
        """Get all records for a specific device"""
        """HARD CODE ORDER AND LIMIT - TODO fix it later"""
        records = (
            db.session.query(Record)
            .filter(Record.device_id == device_id)
            .order_by(desc(Record.created_at))
            .limit(100)
            .all()
        )
        data = [record.as_dict() for record in records]
        return ok_res(data=data)

    def post(self, device_id):
        """Post a record to a specific device"""

        code, res_data = -1, None
        data = request.get_json()
        try:
            distance = float(data.get("distance"))
        except ValidationError as e:
            return error_res(f"Invalid input: {str(e)}")

        try:
            db.session.add(
                record := Record(
                    device_id=device_id,
                    distance=distance,
                    created_at=datetime.datetime.utcnow(),
                )
            )
            db.session.commit()
            code, res_data = 0, {"id": record.id}
            msg = f"Record created for device with id {device_id}"
        except Exception as e:
            db.session.rollback()
            msg = f"Error: {str(e)}"
        finally:
            db.session.close()
        return res(msg, code, res_data)


# adding the defined resources along with their corresponding urls
api.add_resource(DeviceList, "/devices")
api.add_resource(DeviceItem, "/devices/<int:device_id>")
api.add_resource(RecordList, "/records")
api.add_resource(RecordItem, "/records/<int:record_id>")
api.add_resource(DeviceRecords, "/devices/<int:device_id>/records")


if __name__ == "__main__":
    app.run(debug=False, port=5009)
