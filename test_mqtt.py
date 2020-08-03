# MQTT test
# Program Description: 
#   - Simulated message publishing on irisslive MQTT broker
#   - Subscribe / Publish only to RAW message channel

import paho.mqtt.client as mosquitto
import sys
import os
import json
import time
import asyncio
import threading
import random
import argparse

class MQTT_SAMPLE_NODE():
    def __init__(self):
        self.lat1 = None
        self.lat2 = None

        self.lon1 = None
        self.lon2 = None

        self.t1 = None
        self.t2 = None

        self.hum1 = None
        self.hum2 = None

    def message1_raw(self):
        msg1 = {'station': 'BARN1', 'receiver': 'rcvr_1', 'data': {'TIMESTAMP': 1595624982.47, 'ADDR_FROM': 'test', 'RSSI_RX': 93, 'FRAME_TYPE': '0xd2a8', 'FRAME_CNT': 82, 'FRAME': None, 'frame_data': {'packet_id': 53928, 'packet_num': 860, 'epoch index': 860, 'gps_lat': 405363090, 'gps_lon': -1063963796, 'gps_alt': 15578190, 'gps_tow': 508198000, 'gps_fix': 3, 'gps_numsats': 18, 'GOND_BATT': 24, 'GOND_STA': 0, 'RS41_Temp': 0, 'RS41_Hum': 0, 'RS41_Pres': 0, 'RS41_Stat': 0, 'Ta1': 15384, 'Ti1': 41446, 'Ta2': 15771, 'Ti2': 41779, 'CW_CP_Vr1': 511, 'CW_CP_Vr2': 186, 'CW_CP_Vo1': 92, 'CW_CP_Vo2': 4574, 'CW_CP_Cpot': 2, 'CW_CP_Gpot': 255, 'gps_veln': 530, 'gps_vele': 1293, 'gps_veld': 212, 'HW_CP_Vr1': 511, 'HW_CP_Vr2': 478, 'HW_CP_Vo1': 73, 'HW_CP_Vo2': -19589, 'HW_CP_Cpot': 2, 'HW_CP_Gpot': 126, 'gps_rms_hor': 0, 'gps_rms_ver': 0, 'VENT_BATT': 31, 'VENT_STAT': 54, 'VENT_Ta1': 409, 'VENT_Ti1': 47897, 'VENT_Ta2': 409, 'VENT_Ti2': 47590, 'VENT_DIFF': 0, 'GOND_BATT_C': 5.415882352941177, 'VENT_BATT_C': 5.551764705882353, 'Ta1_C': -62.44140625, 'Ti1_C': 1.1865234375, 'Ta2_C': -61.49658203125, 'Ti2_C': 1.99951171875, 'VENT_Ta1_C': None, 'VENT_Ti1_C': 16.93603515625, 'VENT_Ta2_C': None, 'VENT_Ti2_C': 16.1865234375, 'gps_veln_C': 5.3, 'gps_vele_C': 12.93, 'gps_veld_C': 2.12}, 'converted': 1595624982.4692912}}
        return msg1

    def message2_raw(self):
        msg2 = {'station': 'BARN1', 'receiver': 'rcvr_1', 'data': {'TIMESTAMP': 1595624953.35, 'ADDR_FROM': 'test', 'RSSI_RX': 101, 'FRAME_TYPE': '0xc109', 'FRAME_CNT': 81, 'FRAME': None, 'frame_data': {'packet_id': 49417, 'packet_num': 6865, 'epoch index': 858, 'interval index': 1, 'gps_lat': 405350375, 'gps_lon': -1064006728, 'gps_alt': 15638662, 'gps_tow': 508168600, 'gps_fix': 3, 'gps_numsats': 18, 'CW_SA_0': 25127, 'CW_SA_1': 24076, 'CW_SA_2': 22492, 'CW_SA_3': 27592, 'CW_SA_4': 33866, 'CW_SA_5': 37400, 'CW_SA_6': 37888, 'CW_SA_7': 37519, 'CW_SA_8': 38047, 'HW_SA_0': 22705, 'HW_SA_1': 23724, 'HW_SA_2': 22690, 'HW_SA_3': 27127, 'HW_SA_4': 32966, 'HW_SA_5': 38917, 'HW_SA_6': 46102, 'HW_SA_7': 46902, 'HW_SA_8': 47276, 'CW_Vr1': 511, 'CW_Vr2': 478, 'CW_Vo1': 58, 'CW_Vo2': 223, 'CW_Cpot': 56560, 'CW_Gpot': 61496, 'HW_Vr1': 511, 'HW_Vr2': 300, 'HW_Vo1': 18, 'HW_Vo2': 71}}}
        return msg2

    def message1_stat(self):
        msg1 = {
            "station": "TEST_02",
            "stat_time": 1591377410.7666922,
            "receiver_1": {
            "last": {},
            "all": {
                "s0605_1107": {
                "last_update": 1591377409.1559215,
                "par_bytes": 21346,
                "par_pkts": 271,
                "unpar_bytes": 5511,
                "unpar_pkts": 103
                }
            }
            },
            "mqtt": {
            "last_update": 1591377406.7164395,
            "mqtt_qIn": 0,
            "mqtt_qOut": 0,
            "period": 5.055276870727539,
            "mqtt_in": 0,
            "mqtt_out": 4
            },
            "tracker": {
            "time": 1591377410.7666922,
            "gps": {
                "gps_lat": 39.0639,
                "gps_lon": -108.5506,
                "gps_alt": "n/a",
                "gps_fix": "n/a",
                "gps_numsats": 3,
                "gps_time": "n/a",
                "gps_tow": 0,
                "gps_veln": 0,
                "gps_vele": 0,
                "gps_veld": 0
            },
            "ant": {
                "last_update": 0,
                "azm": 90,
                "elv": 0,
                "req_azm": 0,
                "req_elv": 0,
                "volts": 0,
                "curr": 0,
                "status": 0
            },
            "stat": {
                "last_update": 1591376873.0633297
            }
            }
        }
        return msg1

    def message2_stat(self):
        msg2 = {
            "station": "TEST_02",
            "stat_time": 1591377410.7666922,
            "receiver_1": {
            "last": {},
            "all": {
                "s0605_1107": {
                "last_update": 1591377409.1559215,
                "par_bytes": 21346,
                "par_pkts": 271,
                "unpar_bytes": 5511,
                "unpar_pkts": 103
                }
            }
            },
            "mqtt": {
            "last_update": 1591377406.7164395,
            "mqtt_qIn": 0,
            "mqtt_qOut": 0,
            "period": 5.055276870727539,
            "mqtt_in": 0,
            "mqtt_out": 4
            },
            "tracker": {
            "time": 1591377410.7666922,
            "gps": {
                "gps_lat": self.lat2,
                "gps_lon": self.lon2,
                "gps_alt": "n/a",
                "gps_fix": "n/a",
                "gps_numsats": 3,
                "gps_time": "n/a",
                "gps_tow": 0,
                "gps_veln": 0,
                "gps_vele": 0,
                "gps_veld": 0
            },
            "ant": {
                "last_update": 0,
                "azm": 0,
                "elv": 0,
                "req_azm": 0,
                "req_elv": 0,
                "volts": 0,
                "curr": 0,
                "status": 0
            },
            "stat": {
                "last_update": 1591376873.0633297
            }
            }
        }
        return msg2

    def on_connect(self, client, userdata, flags, rc):
        self.connected = True
        print("Connected to %s" % client)

    def on_message(self, client,  userdata, message):
        print(message)

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            self.connected = False
            print("Unexpected disconnection.")
    
    def publish_message_wrap(self, channel, message_func):
        self.mqttc.publish(channel, str(json.dumps(message_func)), qos = 2)

    def logging_test_raw(self):

        t = threading.Timer(2.0, self.logging_test_raw)
        t.daemon = True
        self.random_data()
        msg1 = self.message1_raw()
        msg2 = self.message2_raw()

        self.publish_message_wrap("muri/raw", msg1)
        time.sleep(5)
        self.publish_message_wrap("muri/raw", msg2)
        
        t.start()

    def logging_test_stat(self):

        t = threading.Timer(1.0, self.logging_test_stat)
        t.daemon = True

        self.random_data()
        msg1 = self.message1_stat()
        msg2 = self.message2_stat()

        self.publish_message_wrap("muri/stat", msg1)
        time.sleep(1)
        #self.publish_message_wrap("muri/_test", msg2)
        
        t.start()

    def random_data(self):

        self.lat1 = int(random.uniform(38, 41) * 10000000)
        self.lon1 = int(random.uniform(-103, -106) * 10000000)

        self.lat2 = int(random.uniform(33, 40) * 10000000)
        self.lon2 = int(random.uniform(-104, -107) * 10000000)

        self.t1 = int(random.uniform(0, 1000))
        self.t2 = int(random.uniform(0, 1000))

        self.hum1 = int(random.uniform(0, 1000))
        self.hum2 = int(random.uniform(0, 1000))

        self.rssi1 = int(random.uniform(0, 100))
        self.rssi2 = int(random.uniform(0, 100))

        self.alt1 = int(random.uniform(1000, 20000))
        self.alt2 = int(random.uniform(1000, 20000))

    async def init_mqtt(self, args_stat, args_raw):

        MQTT_USER = "muri"
        MQTT_PASS = "demo2020"
        MQTT_HOST = "irisslive.net"
        MQTT_PORT = 8883

        self.mqttc.username_pw_set(MQTT_USER, MQTT_PASS)

        self.mqttc.on_message = self.on_message
        self.mqttc.on_connect = self.on_connect

        print("Connecting to MQTT Server")
        try:
            self.mqttc.connect(MQTT_HOST, MQTT_PORT)
        except:
            print('Could not connect')

        self.mqttc.loop_start()

        print("Subscribing to Topics")
        self.mqttc.subscribe('muri/raw')
        self.mqttc.subscribe('muri/stat')

        if (args_raw):
            print('!--- Output to muri/raw ---!')
            self.logging_test_raw()
        
        if(args_stat):
            print('!--- Output to muri/stat ---!')
            self.logging_test_stat()

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
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-s', '--stat',
                    action='store_true',
                    help = "Stat message output" )
    group.add_argument('-r', '--raw',
                    action='store_true',
                    help = "Raw message output" )

    args = parser.parse_args()

    mqtt_conn = MQTT_SAMPLE_NODE()

    loop = asyncio.get_event_loop()

    loop.run_until_complete(asyncio.ensure_future(mqtt_conn.init_mqtt(args.stat, args.raw)))