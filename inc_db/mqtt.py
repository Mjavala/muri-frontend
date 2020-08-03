import paho.mqtt.client as mosquitto
import json
import time
import asyncio
import stat_db.stat_msg as decode_stat
import raw_db_0xd2a8.msg_0xd2a8 as decode_0xd
import raw_db_0xc109.msg_0xc109 as decode_0xc

import os
from os.path import join, dirname
from dotenv import load_dotenv
from collections import deque 

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

MQTT_USER = os.getenv('MQTT_USER')
MQTT_PASS = os.getenv('MQTT_PASS')
MQTT_HOST = os.getenv('MQTT_HOST')

class stat_client():

    def __init__(self): 
        #self.app_log_setup = db_log.main_app_logs()
        #self.logger = logging.getLogger('app')
        
        #self.bucket = []
        self.current_message = None

        self.mqttc = mosquitto.Client()
        self.mqttc.on_connect = self.on_mqtt_conn
        self.mqttc.on_disconnect = self.on_mqtt_disc
        self.mqttc.on_message = self.on_mqtt_msg

        self.queue_stat = deque()
        self.queue_0xc = deque() 
        self.queue_0xd = deque()

    def on_mqtt_conn(self, client, userdata, flags, rc):
        try:
            if rc == 0:
                self.connected = True
                self.mqttc.subscribe('muri/stat', qos = 2)   # !-- QoS 2 - message received exactly once --!
                self.mqttc.subscribe('muri/raw', qos = 2)   # !-- QoS 2 - message received exactly once --!
                print("--- MQTT Connected! ---")
            else: 
                self.connected = False
                print("!!! MQTT Connection Failed! !!!")

        except Exception as e:
            print('Error in Connect Callback %s' % e)
    

    def on_mqtt_disc(self, client, userdata, rc): 
        self.connected = False
        if (rc != 0): 
            print("!!! MQTT Disconnceted Unexpectedly !!!")
        else: 
            print("!!! MQTT Disconnceted Planned !!!")
            self.connected = False

    def on_mqtt_msg(self, client,  userdata, message):
        payload = json.loads(str(message.payload.decode()))
        
        if message.topic == 'muri/stat':
            try:
                msg = decode_stat.decode(self, payload)
                self.queue_stat.append(msg)
                
            except Exception as e: 
                print("Error decoding stat message: %s" % e)

        if message.topic == 'muri/raw':
            if payload['data']['FRAME_TYPE'] == '0xd2a8':
                try:
                    msg = decode_0xd.decode(self, payload)
                    self.queue_0xd.append(msg)

                except Exception as e: 
                    print("Error decoding 0xd2a8 message: %s" % e)

            if payload['data']['FRAME_TYPE'] == '0xc109':
                try:
                    msg = decode_0xc.decode(self, payload)
                    self.queue_0xc.append(msg)

                except Exception as e: 
                    print("Error decoding 0xd2a8 message: %s" % e)

    def get_queue_stat(self):
        return self.queue_stat

    def get_queue_0xd2a8(self):
        return self.queue_0xd

    def get_queue_0xc109(self):
        return self.queue_0xc

    async def start_mqtt(self):
        try:
            self.mqttc.username_pw_set(MQTT_USER, MQTT_PASS)
            self.mqttc.connect_async(MQTT_HOST, 8883, keepalive=15)
            self.mqttc.loop_start()

        except Exception as e: 
            print("Exception in MQTT Start Script: %s" % e)

    async def main_loop(self):
        last_time = time.time()
        try: 
            await self.start_mqtt()
            while(True):
                if (time.time() - last_time > 1):
                    last_time = time.time()

                await asyncio.sleep(0.1)

        except Exception as e:
            print("Exception in MQTT loop: %s" % e)


if __name__ == "__main__":
    mqtt_conn = mqtt_client()
    
    loop = asyncio.get_event_loop()

    tasks = [asyncio.ensure_future(mqtt_conn.main_loop())]

    loop.run_until_complete(asyncio.gather(*tasks))
