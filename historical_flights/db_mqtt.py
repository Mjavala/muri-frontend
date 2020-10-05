import paho.mqtt.client as mosquitto
import json
import time
import asyncio
import logging
import db_log
from datetime import datetime
import pytz
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '/root/muri/.env')    # depends on your directory structure
load_dotenv(dotenv_path)

MQTT_USER = os.getenv('MQTT_USER')
MQTT_PASS = os.getenv('MQTT_PASS')
MQTT_HOST = os.getenv('MQTT_HOST')

class muri_app_mqtt():

    def __init__(self): 
        self.app_log_setup = db_log.main_app_logs()
        self.logger = logging.getLogger('app')
        
        self.bucket = []
        self.current_message = None

        self.mqttc = mosquitto.Client()
        self.mqttc.on_connect = self.on_mqtt_conn
        self.mqttc.on_disconnect = self.on_mqtt_disc
        self.mqttc.on_message = self.on_mqtt_msg

        self.live = False
        self.t0 = None

        # metadata
        self.timestamp = None
        self.id = None
        self.station = None
        self.altitude = None
        self.latitude = None
        self.longitude = None
        self.frame = None
        self.frame_type = None
        self.packet_id = None
        self.gps_tow = None
        # 0xd2a8 packet type
        self.temp = None
        self.batt_mon = None
        self.vent_batt = None
        self.ta1_c = None 
        self.ti1_c = None   
        self.ti2_c = None   
        # station message packet
        self.slant = None
        self.rssi = None
        # 0xc109 packet
        self.hw_vo1 = None
        self.hw_vo2 = None
        self.cw_vo1 = None
        self.cw_vo2 = None


    def on_mqtt_conn(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            self.mqttc.subscribe('muri/raw', qos = 2)   # !-- QoS 2 - message received exactly once --!
            self.mqttc.subscribe('muri/stat', qos = 2)   # !-- QoS 2 - message received exactly once --!
            self.logger.log_app("--- MQTT Connected! ---")
        else: 
            self.connected = False
            self.logger.log_app("!!! MQTT Connection Failed! !!!")

    def on_mqtt_disc(self, client, userdata, rc): 
        self.connected = False
        if (rc != 0): 
            self.logger.log_app("!!! MQTT Disconnceted Unexpectedly !!!")
        else: 
            self.logger.log_app("!!! MQTT Disconnceted Planned !!!")
            self.connected = False

    def on_mqtt_msg(self, client,  userdata, message):
        # need to call the the status function in main every second
        payload = json.loads(str(message.payload.decode()))

        if message.topic == 'muri/stat':
            if self.live:
                self.clear_raw_data()
                self.rssi = payload['receiver_1']['last']['rssi_last']['rssi']
                self.slant = payload['tracker']['track']['last_slant']
                self.timestamp_to_datetime(payload['stat_time'])
                self.station = payload['station']
                self.stats()
        #self.msg_to_db_raw = payload
        if message.topic == 'muri/raw':
            if payload['data']['frame_data']:
                result = self.simulation_check(payload['data']['ADDR_FROM'])
                if result:
                    self.live = True
                    self.t0 = time.time()
                    self.clear_stat_data()
                    self.db_data(payload)
                    self.stats()

    def db_data(self, payload):
            self.timestamp_to_datetime(payload['data']['TIMESTAMP'])
            self.station = payload['station']
            self.id = payload['data']['ADDR_FROM']
            self.latitude = (payload['data']['frame_data']['gps_lat'] / 10000000)
            self.longitude = (payload['data']['frame_data']['gps_lon'] / 10000000)
            self.altitude = (payload['data']['frame_data']['gps_alt'] / 1000)
            self.frame_type = payload['data']['FRAME_TYPE']
            self.packet_id = payload['data']['frame_data']['packet_id']
            self.gps_tow = payload['data']['frame_data']['gps_tow']
            self.frame = payload['data']['FRAME']

            #self.rssi = payload['data']['RSSI_RX']
            if payload['data']['FRAME_TYPE'] == '0xd2a8':
                self.clear_0xc109()
                self.batt_mon = round(payload['data']['frame_data']['GOND_BATT_C'], 4)
                self.vent_batt = payload['data']['frame_data']['VENT_BATT_C']
                if (payload['data']['frame_data']['Ta2_C']):
                    self.temp = round(payload['data']['frame_data']['Ta2_C'], 4)
                    self.ta1_c = round(payload['data']['frame_data']['Ta1_C'], 4)
                    self.ti1_c = round(payload['data']['frame_data']['Ti1_C'], 4)
                    self.ti2_c = round(payload['data']['frame_data']['Ti2_C'], 4)

            if payload['data']['FRAME_TYPE'] == '0xc109':
                self.clear_0xd2a8()
                self.hw_vo1 = (payload['data']['frame_data']['HW_Vo1'] / -4680) + 14
                self.hw_vo2 = (payload['data']['frame_data']['HW_Vo2'] / -4680) + 14
                self.cw_vo1 = (payload['data']['frame_data']['CW_Vo1'] / -4680) + 14
                self.cw_vo2 = (payload['data']['frame_data']['CW_Vo2'] / -4680) + 14

    def timestamp_to_datetime(self, ts):
        tz = pytz.timezone('America/Denver')
        dt = datetime.fromtimestamp(ts, tz).strftime('%Y-%m-%d %H:%M:%S')
        self.timestamp = dt

    def simulation_check(self, addr_from):
        # TODO: FIX this hack pls (REGEX)
        result = addr_from.startswith('x')
        if result:
            return result
        elif not result:
            return result

    def bucket_to_db(self):
        sent = False
        try:
            if len(self.bucket) >= 5:
                sent = True
                return self.bucket
            else:
                return False
        finally:
            if sent:
                self.bucket = []


    def stats(self):
        self.current_message = (
            self.timestamp,
            self.id,
            self.station,
            self.latitude,
            self.longitude,
            self.altitude,
            self.rssi,
            self.temp,
            self.batt_mon,
            self.vent_batt,
            self.frame_type,
            self.packet_id,
            self.ta1_c,
            self.ti1_c,
            self.ti2_c,
            self.gps_tow,
            self.frame,
            self.slant,
            self.hw_vo1,
            self.hw_vo2,
            self.cw_vo1,
            self.cw_vo2

        )
        self.bucket.append(self.current_message)

    def clear_raw_data(self):
        self.latitude = None
        self.longitude = None
        self.altitude = None
        self.temp = None
        self.batt_mon = None
        self.vent_batt = None
        self.frame_type = None
        self.packet_id = None
        self.ta1_c = None
        self.ti1_c = None
        self.ti2_c = None
        self.gps_tow = None
        self.frame = None
        self.cw_vo1 = None
        self.cw_vo2 = None
        self.hw_vo1 = None
        self.hw_vo2 = None

    def clear_0xc109(self):
        self.cw_vo1 = None
        self.cw_vo2 = None
        self.hw_vo1 = None
        self.hw_vo2 = None

    def clear_0xd2a8(self):
        self.temp = None
        self.batt_mon = None
        self.vent_batt = None
        self.ta1_c = None 
        self.ti1_c = None   
        self.ti2_c = None  

    def clear_stat_data(self):
        self.rssi = None
        self.slant = None

    def live_flight(self):
        return self.live

    async def start_mqtt(self):
    
        try:
            self.mqttc.username_pw_set(MQTT_USER, MQTT_PASS)

            self.logger.log_app("Connecting to MQTT Server....")
            self.mqttc.connect_async(MQTT_HOST, 8883, keepalive=15)
            self.mqttc.loop_start()

        except Exception as e: 
            self.logger.log_app("Exception in MQTT Start Script: %s" % e)

    async def main_loop(self):
        last_time = time.time()
        try: 
            await self.start_mqtt()
            while(True):
                if (self.live == True):
                    if (time.time() - self.t0 > 60):
                        self.live = False

                await asyncio.sleep(0.1)
        except Exception as e:
            self.logger.log_app.log_app("Exception in MQTT: %s" % e)
        finally: 
            pass


if __name__ == "__main__":
    mqtt_conn = muri_app_mqtt()

    loop = asyncio.get_event_loop()

    loop.run_until_complete(asyncio.ensure_future(mqtt_conn.main_loop()))

