from paho.mqtt.publish import single


if __name__ == "__main__":
    single(
        'sdispensor',
        payload='1_10',
        qos=1,
        hostname='3.27.67.131',
        port=2885,
        auth = {'username': 'cits5506', 'password': 'atifmansoor'}
    )
