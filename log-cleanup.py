import json
import paho.mqtt.client as mosquitto
MQTT_USER = "muri"
MQTT_PASS = "demo2020"
MQTT_HOST = "irisslive.net"
MQTT_PORT = 8883

try:
    mqttc = mosquitto.Client()
    mqttc.connect(MQTT_HOST, MQTT_PORT)


    with open('9-10-log.json', 'r+') as f:
        print('ello')
        for line in f:
            try:
                mqttc.publish(str(json.dumps(line)), qos = 2)
            except Exception as e:
                print(e)

except Exception as e:
    print(e)
