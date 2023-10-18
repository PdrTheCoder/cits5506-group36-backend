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
* Additionally view a list records by device
  * `GET /devices/<id>/records` - Get all records for a device

#### Components

API Backend utilising Flask and Python

* Flask-RESTful for API generation
* Flask-Pydantic for data validation
* Flask-SQLAlchemy for models and database
* Flask-Cors for cors issue


### Database  

Sqlite3 is used in this project.

Initiate database  
`Python initdb.py`

Also, need to manually create a trigger after initiation.  
`CREATE TRIGGER AUTOUPDATER AFTER INSERT ON record`  
`BEGIN`  
`UPDATE device SET distance = NEW.distance, updated_at = NEW.created_at WHERE id=NEW.device_id;`  
`END;`
