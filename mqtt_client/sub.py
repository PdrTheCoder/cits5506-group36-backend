import paho.mqtt.client as mqtt
import requests
import logging

from send import sendmail

BASE_URL = 'http://127.0.0.1:5009'

# this dict is used for alarm suppression
alert_log = {
    1: False,
    2: False,
    3: False,
    4: False,
    5: False,
    6: False,
    7: False,
    8: False,
    9: False,
    10: False,
    11: False,
    12: False,
    13: False,
    14: False,
    15: False,
    16: False,
    17: False,
    18: False
}

logger = logging.getLogger(__name__)

def callback_data_report(client, userdata, msg):
    global alert_log

    # parse parameters
    try:
        device_id = int((tmp := msg.payload.decode().split('_'))[0])
        distance = round(float(tmp[1]), 1)
        print(f'device_id: {device_id}, distance: {distance}.')
    except Exception as e:
        logger.error(f'Error: {str(e)}')

    # post to record
    try:
        # TODO also need to use device local time, here just ignore that
        res = requests.post(
            f'{BASE_URL}/devices/{device_id}/records',
            json={'distance': distance},
            headers={"Content-Type": "application/json"})
        data = res.json()
        print(data['message'])
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return

    # HERE we compare the threshold and distance
    # TODO
    try:
        res1 = requests.get(
            f'{BASE_URL}/devices/1'
        )
        data = res1.json()
        if data['code'] == 0:
            threshold = float(data['data']['threshold'])
            device_name = data['data']['name']
            print(f'threshold - {threshold}')
        else:
            raise Exception(data['message'])
    except Exception as e:
        # TODO
        logger.error(f'Error: {str(e)}')

    # alert suppression
    if distance >= threshold:
        if not alert_log[device_id]:
            # send email
            try:
                sendmail(
                    ', '.join(['23870387@student.uwa.edu.au', 'jpatrickbraunagel@gmail.com']),
                    f'Wake up mate, you got to refill the toilet paper - {device_name}',
                    f'Dispenser - {device_id} is running out.')
                # revert the flag
                alert_log[device_id] = True
            except Exception as e:
                print(str(e))
    else:
        # reset flag state
        alert_log[device_id] = False
    print('finished.')


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
