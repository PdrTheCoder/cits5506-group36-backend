from datetime import datetime
import paho.mqtt.client as mqtt
import requests
import sqlite3

conn = sqlite3.connect('../instance/project.db')
URL = 'http://127.0.0.1/devices/'

alert_log = {
    1: False,
    2: False,
    3: False
}

def callback_data_report(client, userdata, msg):
    try:
        device_id = int((tmp := msg.payload.decode().split('_'))[0])
        distance = round(float(tmp[1]), 1)
        # TODO also need to use device local time, here just ignore that
        res = requests.post(
            f'http://127.0.0.1/devices/{device_id}/records',
            data={'distance': distance},
            headers={"Content-Type": "application/json"})

    except Exception as e:
        # TODO 
        print(str(e))
    
    # HERE we compare the threshold and distance
    # TODO


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe([("sdispensor", 1)])
    client.message_callback_add("sdispensor", callback_data_report)


client = mqtt.Client('toiletpaper', clean_session=False)

# HARD CODE credentials ... dangerous
client.username_pw_set('cits5506', 'atifmansoor')
client.on_connect = on_connect
client.connect('127.0.0.1', 2885, 60)
client.loop_forever()
