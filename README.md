# CITS5506 IoT Project

## Group 36

### Backend

#### Features

* API for CRUD operations on devices and records
  * `GET /devices` - Get all devices
  * `GET /devices/<id>` - Get device by id
  * `POST /devices` - Create a new device
  * `PATCH /devices/<id>` - Update a device
  * `DELETE /devices/<id>` - Delete a device
  * `GET /records` - Get all records
  * `GET /records/<id>` - Get record by id
  * `POST /records` - Create a new record
  * `PATCH /records/<id>` - Update a record
  * `DELETE /records/<id>` - Delete a record

#### Components

API Backend utilising Flask and Python

* Flask-RESTful for API generation
* Flask-Pydantic for data validation
* Flask-SQLAlchemy for models and database
