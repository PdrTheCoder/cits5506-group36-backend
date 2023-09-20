# using flask_restful
from flask import Flask, jsonify, request
from flask_restful import Resource, Api

from model import db, Device
from utils import ok_res
from utils import error_res


# creating the flask app
app = Flask(__name__)

# configure database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

# creating an API object
api = Api(app)


class DeviceListRes(Resource):
  
    def get(self):
        # get all devices
        return jsonify({'message': 'todo'})
  
    def post(self):
        # register a device

        args_json = request.get_json()
        # TODO sanitize arguments

        new_device = Device(
            name=args_json.get('name'),
            desc=args_json.get('desc'),
            empty_distance=args_json.get('empty_distance'),
            threshold=args_json.get("threshold")
        )

        try:
            db.session.add(new_device)
            db.session.commit()
        except Exception as e:
            db.session.close()
            return error_res(f'Fail to register the device. Reason: {str(e)}')
        return ok_res(data={"id": new_device.id})
  
  
# another resource to calculate the square of a number
class DeviceRes(Resource):
  
    def patch(self):
        # update a device
        return jsonify({'message': 'todo'})
    
    def delete(self):
        # delete a device
        return jsonify({'message': 'todo'})
  
  
# adding the defined resources along with their corresponding urls
api.add_resource(DeviceListRes, '/devices')
api.add_resource(DeviceRes, '/devices/<int:num>')
  
  
if __name__ == '__main__':
    app.run(debug = True)
