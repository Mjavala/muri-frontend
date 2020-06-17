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
        msg1 = {
            "station": "TEST_01",
            "receiver": "rcvr_1",
            "data": {
                "TIMESTAMP": 1588353888.8910325,
                "ADDR_FROM": "test2",
                "RSSI_RX": self.rssi1,
                "FRAME_TYPE": "0xd2a8",
                "FRAME_CNT": 70,
                "FRAME": "d2a84e6d4e6d17bedcc3c14ee650001ac9f51d7c94b80315c7010000000000000000999999999999999901ff00ba0000ffff02fffffc0000fffd01ff01de011c0000027e0000",
                "frame_data": {
                "packet_id": 53928,
                "packet_num": 20077,
                "epoch index": 20077,
                "gps_lat": self.lat1,
                "gps_lon": self.lon1,
                "gps_alt": self.alt1,
                "gps_tow": 494703800,
                "gps_fix": 3,
                "gps_numsats": 21,
                "Batt Mon": 199,
                "Gondola Statu": 1,
                "RS41 Temp": 0,
                "RS41 Hum": self.hum1,
                "RS41 Pres": 0,
                "temp Ta1 (amb)": self.t1,
                "temp Ti1 (int)": 39321,
                "temp Ta2 (amb)": 39321,
                "temp Ti2 (int)": 39321,
                "CW Chop Vr1": 39321,
                "CW Chop Vr2": 511,
                "CW Chop Vo1": 186,
                "CW Chop Vo2": 0,
                "CW Chop Cpot": 65535,
                "CW Chop Gpot": 2,
                "gps_veln": 255,
                "gps_vele": -4,
                "gps_vel_d": 0,
                "HW Chop Vr1": -3,
                "HW Chop Vr2": 511,
                "HW Chop Vo1": 478,
                "HW Chop Vo2": 284,
                "HW Chop Cpot": 0,
                "HW Chop Gpot": 2,
                "RMS Hor Vel": 126,
                "RMS Ver Vel": 0,
                "var_35": 0
                }
            }
        }
        return msg1

    def message2_raw(self):
        msg2 = {
            "station": "TEST_01",
            "receiver": "rcvr_1",
            "data": {
                "TIMESTAMP": 1588353888.8910325,
                "ADDR_FROM": "test1",
                "RSSI_RX": self.rssi2,
                "FRAME_TYPE": "0xd2a8",
                "FRAME_CNT": 70,
                "FRAME": "d2a84e6d4e6d17bedcc3c14ee650001ac9f51d7c94b80315c7010000000000000000999999999999999901ff00ba0000ffff02fffffc0000fffd01ff01de011c0000027e0000",
                "frame_data": {
                "packet_id": 53928,
                "packet_num": 20077,
                "epoch index": 20077,
                "gps_lat": self.lat2,
                "gps_lon": self.lon2,
                "gps_alt": self.alt2,
                "gps_tow": 494703800,
                "gps_fix": 3,
                "gps_numsats": 21,
                "Batt Mon": 199,
                "Gondola Statu": 1,
                "RS41 Temp": 0,
                "RS41 Hum": self.hum2,
                "RS41 Pres": 0,
                "temp Ta1 (amb)": self.t2,
                "temp Ti1 (int)": 39321,
                "temp Ta2 (amb)": 39321,
                "temp Ti2 (int)": 39321,
                "CW Chop Vr1": 38321,
                "CW Chop Vr2": 511,
                "CW Chop Vo1": 186,
                "CW Chop Vo2": 0,
                "CW Chop Cpot": 65535,
                "CW Chop Gpot": 2,
                "gps_veln": 255,
                "gps_vele": -4,
                "gps_vel_d": 0,
                "HW Chop Vr1": -3,
                "HW Chop Vr2": 511,
                "HW Chop Vo1": 478,
                "HW Chop Vo2": 284,
                "HW Chop Cpot": 0,
                "HW Chop Gpot": 2,
                "RMS Hor Vel": 126,
                "RMS Ver Vel": 0,
                "var_35": 0
                }
            }
        }
        return msg2

    def message1_stat(self):
        msg1 = {
            "station": "TEST_01",
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
                "gps_lat": self.lat1,
                "gps_lon": self.lon1,
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

        t = threading.Timer(1.0, self.logging_test_raw)
        t.daemon = True
        self.random_data()
        msg1 = self.message1_raw()
        msg2 = self.message2_raw()

        self.publish_message_wrap("muri/raw", msg1)
        time.sleep(1)
        self.publish_message_wrap("muri/raw", msg2)
        
        t.start()

    def logging_test_stat(self):

        t = threading.Timer(1.0, self.logging_test_stat)
        t.daemon = True

        self.random_data()
        msg1 = self.message1_stat()
        msg2 = self.message2_stat()

        self.publish_message_wrap("muri/_test", msg1)
        time.sleep(1)
        self.publish_message_wrap("muri/_test", msg2)
        
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