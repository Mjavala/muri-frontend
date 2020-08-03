import paho.mqtt.client as mosquitto
import json
import time
import asyncio
import raw_db_0xc109.write_db_0xc as write
import os
from os.path import join, dirname
from dotenv import load_dotenv
from collections import deque 

dotenv_path = join(dirname(__file__), '../../.env')
load_dotenv(dotenv_path)

MQTT_USER = os.getenv('MQTT_USER')
MQTT_PASS = os.getenv('MQTT_PASS')
MQTT_HOST = os.getenv('MQTT_HOST')

class mqtt_0xc():

    def __init__(self): 
        
        self.current_message = None
        self.write_0xc = write.db_0xc109()

        self.mqttc = mosquitto.Client()
        self.mqttc.on_connect = self.on_mqtt_conn
        self.mqttc.on_disconnect = self.on_mqtt_disc
        self.mqttc.on_message = self.on_mqtt_msg

        self.queue = deque()        

        self.station = None
        self.receiver = None
        self.timestamp = None
        self.addr_from = None
        self.rssi = None
        self.frame_type = None
        self.frame_cnt = None
        self.frame = None
        self.packet_id = None
        self.packet_num = None
        self.epoch_index = None
        self.interval_index = None
        self.gps_lat = None
        self.gps_lon = None
        self.gps_alt = None
        self.gps_tow = None
        self.gps_fix = None
        self.gps_numsats = None
        self.cw_sa_0 = None
        self.cw_sa_1 = None
        self.cw_sa_2 = None
        self.cw_sa_3 = None
        self.cw_sa_4 = None
        self.cw_sa_5 = None
        self.cw_sa_6 = None
        self.cw_sa_7 = None
        self.cw_sa_8 = None
        self.hw_sa_0 = None
        self.hw_sa_1 = None
        self.hw_sa_2 = None
        self.hw_sa_3 = None
        self.hw_sa_4 = None
        self.hw_sa_5 = None
        self.hw_sa_6 = None
        self.hw_sa_7 = None
        self.hw_sa_8 = None
        self.cw_vr1 = None
        self.cw_vr2 = None
        self.cw_vo1 = None
        self.cw_vo2 = None
        self.cw_cpot = None
        self.cw_gpot = None
        self.hw_vr1 = None
        self.hw_vr2 = None
        self.hw_vo1 = None
        self.hw_vo2 = None

    def on_mqtt_conn(self, client, userdata, flags, rc):
        try:
            if rc == 0:
                self.connected = True
                self.mqttc.subscribe('muri/raw', qos = 2)   # !-- QoS 2 - message received exactly once --!
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
        
        if message.topic == 'muri/raw':
            if payload['data']['FRAME_TYPE'] == '0xc109':
                self.stat_db_data(payload)
                self.stat_db_msg()

    def stat_db_data(self, payload):
        try:
            self.station = payload['station']
            self.receiver = payload['receiver']
            self.timestamp = payload['data']['TIMESTAMP']
            self.addr_from = payload['data']['ADDR_FROM']
            self.rssi = payload['data']['RSSI_RX']
            self.frame_type = payload['data']['FRAME_TYPE']
            self.frame_cnt = payload['data']['FRAME_CNT']
            self.frame = payload['data']['FRAME']
            self.packet_id = payload['data']['frame_data']['packet_id']
            self.packet_num = payload['data']['frame_data']['packet_num']
            self.epoch_index = payload['data']['frame_data']['epoch index']
            self.interval_index = payload['data']['frame_data']['interval index']
            self.gps_lat = payload['data']['frame_data']['gps_lat']
            self.gps_lon = payload['data']['frame_data']['gps_lon']
            self.gps_alt = payload['data']['frame_data']['gps_alt']
            self.gps_tow = payload['data']['frame_data']['gps_tow']
            self.gps_fix = payload['data']['frame_data']['gps_fix']
            self.gps_numsats = payload['data']['frame_data']['gps_numsats']
            self.cw_sa_0 = payload['data']['frame_data']['CW_SA_0']
            self.cw_sa_1 = payload['data']['frame_data']['CW_SA_1']
            self.cw_sa_2 = payload['data']['frame_data']['CW_SA_2']
            self.cw_sa_3 = payload['data']['frame_data']['CW_SA_3']
            self.cw_sa_4 = payload['data']['frame_data']['CW_SA_4']
            self.cw_sa_5 = payload['data']['frame_data']['CW_SA_5']
            self.cw_sa_6 = payload['data']['frame_data']['CW_SA_6']
            self.cw_sa_7 = payload['data']['frame_data']['CW_SA_7']
            self.cw_sa_8 = payload['data']['frame_data']['CW_SA_8']
            self.hw_sa_0 = payload['data']['frame_data']['HW_SA_0']
            self.hw_sa_1 = payload['data']['frame_data']['HW_SA_1']
            self.hw_sa_2 = payload['data']['frame_data']['HW_SA_2']
            self.hw_sa_3 = payload['data']['frame_data']['HW_SA_3']
            self.hw_sa_4 = payload['data']['frame_data']['HW_SA_4']
            self.hw_sa_5 = payload['data']['frame_data']['HW_SA_5']
            self.hw_sa_6 = payload['data']['frame_data']['HW_SA_6']
            self.hw_sa_7 = payload['data']['frame_data']['HW_SA_7']
            self.hw_sa_8 = payload['data']['frame_data']['HW_SA_8']
            self.cw_vr1 = payload['data']['frame_data']['CW_Vr1']
            self.cw_vr2 = payload['data']['frame_data']['CW_Vr2']
            self.cw_vo1 = payload['data']['frame_data']['CW_Vo1']
            self.cw_vo2 = payload['data']['frame_data']['CW_Vo2']
            self.cw_cpot = payload['data']['frame_data']['CW_Cpot']
            self.cw_gpot = payload['data']['frame_data']['CW_Gpot']
            self.hw_vr1 = payload['data']['frame_data']['HW_Vr1']
            self.hw_vr2 = payload['data']['frame_data']['HW_Vr2']
            self.hw_vo1 = payload['data']['frame_data']['HW_Vo1']
            self.hw_vo2 = payload['data']['frame_data']['HW_Vo2']

        except Exception as e:
            print('Could not parse object %s' % e)

    def stat_db_msg(self):
        try:
            self.current_message = (
                self.station,
                self.receiver,
                self.timestamp,
                self.addr_from,
                self.rssi,
                self.frame_type,
                self.frame_cnt,
                self.frame,
                self.packet_id,
                self.packet_num,
                self.epoch_index,
                self.interval_index,
                self.gps_lat,
                self.gps_lon,
                self.gps_alt,
                self.gps_tow,
                self.gps_fix,
                self.gps_numsats,
                self.cw_sa_0,
                self.cw_sa_1,
                self.cw_sa_2,
                self.cw_sa_3,
                self.cw_sa_4,
                self.cw_sa_5,
                self.cw_sa_6,
                self.cw_sa_7,
                self.cw_sa_8,
                self.hw_sa_0,
                self.hw_sa_1,
                self.hw_sa_2,
                self.hw_sa_3,
                self.hw_sa_4,
                self.hw_sa_5,
                self.hw_sa_6,
                self.hw_sa_7,
                self.hw_sa_8,
                self.cw_vr1,
                self.cw_vr2,
                self.cw_vo1,
                self.cw_vo2,
                self.cw_cpot,
                self.cw_gpot,
                self.hw_vr1,
                self.hw_vr2,
                self.hw_vo1,
                self.hw_vo2
            )
            
            self.queue.append(self.current_message)

        except Exception as e:
            print("Exception in stat_db_msg func: %s" % e)

    def get_queue(self):
        return self.queue

    async def start_mqtt(self):
        try:
            self.mqttc.username_pw_set(MQTT_USER, MQTT_PASS)

            print("Connecting to MQTT Server....")
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
                    await self.write_0xc.msg_in(self.queue)

                await asyncio.sleep(0.1)

        except Exception as e:
            print("Exception in MQTT loop: %s" % e)


if __name__ == "__main__":
    mqtt_conn = mqtt_client()
    
    stat_write_loop = write.muri_db_stat()

    loop = asyncio.get_event_loop()

    tasks = [asyncio.ensure_future(mqtt_conn.main_loop())]

    loop.run_until_complete(asyncio.gather(*tasks))
