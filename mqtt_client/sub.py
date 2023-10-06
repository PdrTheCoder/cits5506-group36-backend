from datetime import datetime
import paho.mqtt.client as mqtt
import sqlite3

conn = sqlite3.connect('../instance/project.db')

def callback_data_report(client, userdata, msg):

    try:
        device_id = int((tmp := msg.payload.decode().split('_'))[0])
        distance = round(float(tmp[1]), 1)
        created_at = datetime.utcnow().isoformat(sep=' ')

        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO record (device_id, distance, created_at) VALUES ({device_id}, {distance}, '{created_at}')")
        cursor.execute(f"UPDATE device SET distance={distance} WHERE id={device_id}")
        conn.commit()
    except Exception as e:
        # TODO 
        print(str(e))


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
