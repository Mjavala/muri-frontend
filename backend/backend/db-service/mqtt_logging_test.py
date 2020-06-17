import paho.mqtt.client as mosquitto
import sys
import os
import json
import time
import asyncio
import threading
import muri_logging

msg1 = {
    "TIMESTAMP": 1587093142.3168666,
    "ADDR_FROM": "test1",
    "RSSI_RX": 40,
    "FRAME_TYPE": "0xc109",
    "FRAME_CNT": 81,
    "FRAME": "c1099f7bf3ef0317bedb09c14ee50f001a95dd1a702eb00312ffffffffffffffffffffffffffffffffffff45c24749552f58476a78727d776780198da901ff01de00000000f03801ff012c3f6f0000fe7e",
    "frame_data": {
        "packet_id": 49417,
        "packet_num": 40827,
        "epoch index": 62447,
        "interval index": 3,
        "GPS Lat": 398383881,
        "GPS Lon": -1051794161,
        "GPS Alt": 1742301,
        "GPS TOW": 443559600,
        "GPS fix type": 3,
        "GPS num sats": 18,
        "CW SA 0": 65535,
        "CW SA 1": 65535,
        "CW SA 2": 65535,
        "CW SA 3": 65535,
        "CW SA 4": 65535,
        "CW SA 5": 65535,
        "CW SA 6": 65535,
        "CW SA 7": 65535,
        "CW SA 8": 65535,
        "HW SA 0": 17858,
        "HW SA 1": 18249,
        "HW SA 2": 21807,
        "HW SA 3": 22599,
        "HW SA 4": 27256,
        "HW SA 5": 29309,
        "HW SA 6": 30567,
        "HW SA 7": 32793,
        "HW SA 8": 36265,
        "CW Meas Vr1": 511,
        "CWMeas Vr2": 478,
        "CW Meas Vo1": 0,
        "CWMeas Vo2": 0,
        "CW Meas Cpot": 0,
        "CW Meas Gpot": 61496,
        "HW Meas Vr1": 511,
        "HW Meas Vr2": 300,
        "HW Meas Vo1": 63,
        "HW Meas Vo2": 111
        }
    }
msg2 = {
    "TIMESTAMP": 1587093142.3168666,
    "ADDR_FROM": "test2",
    "RSSI_RX": 40,
    "FRAME_TYPE": "0xc109",
    "FRAME_CNT": 81,
    "FRAME": "c1099f7bf3ef0317bedb09c14ee50f001a95dd1a702eb00312ffffffffffffffffffffffffffffffffffff45c24749552f58476a78727d776780198da901ff01de00000000f03801ff012c3f6f0000fe7e",
    "frame_data": {
        "packet_id": 49417,
        "packet_num": 40827,
        "epoch index": 62447,
        "interval index": 3,
        "GPS Lat": 398383881,
        "GPS Lon": -1051794161,
        "GPS Alt": 1742301,
        "GPS TOW": 443559600,
        "GPS fix type": 3,
        "GPS num sats": 18,
        "CW SA 0": 65535,
        "CW SA 1": 65535,
        "CW SA 2": 65535,
        "CW SA 3": 65535,
        "CW SA 4": 65535,
        "CW SA 5": 65535,
        "CW SA 6": 65535,
        "CW SA 7": 65535,
        "CW SA 8": 65535,
        "HW SA 0": 17858,
        "HW SA 1": 18249,
        "HW SA 2": 21807,
        "HW SA 3": 22599,
        "HW SA 4": 27256,
        "HW SA 5": 29309,
        "HW SA 6": 30567,
        "HW SA 7": 32793,
        "HW SA 8": 36265,
        "CW Meas Vr1": 511,
        "CWMeas Vr2": 478,
        "CW Meas Vo1": 0,
        "CWMeas Vo2": 0,
        "CW Meas Cpot": 0,
        "CW Meas Gpot": 61496,
        "HW Meas Vr1": 511,
        "HW Meas Vr2": 300,
        "HW Meas Vo1": 63,
        "HW Meas Vo2": 111
        }
    }

class MQTT_SAMPLE_NODE():

    def on_connect(self, client, userdata, flags, rc):
        self.connected = True
        print("Connected to %s" % client)

    def on_message(self, client,  userdata, message):
        print(str(message.payload.decode()))

    def on_disconnect(client, userdata, rc):
        if rc != 0:
            self.connected = False
            print("Unexpected disconnection.")
    
    def on_subscribe(client, userdata, mid, granted_qos):
        pass

    
    def publish_message_wrap(self, channel, message_func):
        self.mqttc.publish(channel, str(json.dumps(message_func)), qos = 2)

    def logging_test(self):

        t = threading.Timer(1.0, self.logging_test)
        t.daemon = True

        self.publish_message_wrap("muri/test", msg1)
        self.publish_message_wrap("muri/test", msg2)
        
        t.start()

    def message_unpack(self, payload):
        try:
            message = json.loads(payload)
        except:
            print('hello world')

        self.id = self.id_set
        self.id.add(message['ADDR_FROM'])

        muri_logging.logger_generator(self.id, message['ADDR_FROM'], payload)

    async def init_mqtt(self):

        MQTT_USER = "muri"
        MQTT_PASS = "demo2020"
        MQTT_HOST = "irisslive.net"
        MQTT_PORT = 8883

        self.mqttc.username_pw_set(MQTT_USER, MQTT_PASS)

        self.mqttc.on_message = self.on_message
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_subscribe = self.on_subscribe

        print("Connecting to MQTT Server")
        try:
            self.mqttc.connect(MQTT_HOST, MQTT_PORT)
        except:
            print('Could not connect')

        self.mqttc.loop_start()

        print("Subscribing to Topics")
        self.mqttc.subscribe('muri/test')

        self.logging_test()

        while (self.connected):
            pass



    def __init__(self): 
        self.mqttc = mosquitto.Client()
        self.id = None
        self.id_set = set()
        self.message_throttle = 0
        self.connected = True

        self.timestamp = None


if __name__ == "__main__":
    mqtt_conn = MQTT_SAMPLE_NODE()

    loop = asyncio.get_event_loop()

    loop.run_until_complete(asyncio.ensure_future(mqtt_conn.init_mqtt()))

