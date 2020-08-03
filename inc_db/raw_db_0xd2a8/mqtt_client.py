import paho.mqtt.client as mosquitto
import json
import time
import asyncio
import raw_db_0xd2a8.write_db_0xd as write_stat
import os
from os.path import join, dirname
from dotenv import load_dotenv
from collections import deque 

dotenv_path = join(dirname(__file__), '../../.env')
load_dotenv(dotenv_path)

MQTT_USER = os.getenv('MQTT_USER')
MQTT_PASS = os.getenv('MQTT_PASS')
MQTT_HOST = os.getenv('MQTT_HOST')

class mqtt_0xd():

    def __init__(self): 
        #self.app_log_setup = db_log.main_app_logs()
        #self.logger = logging.getLogger('app')
        
        self.current_message = None
        self.write_stat = write_stat.db_0xd2a8()

        self.mqttc = mosquitto.Client()
        self.mqttc.on_connect = self.on_mqtt_conn
        self.mqttc.on_disconnect = self.on_mqtt_disc
        self.mqttc.on_message = self.on_mqtt_msg

        self.queue = deque()        

        # stat message definition
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
        self.gps_lat = None
        self.gps_lon = None
        self.gps_alt = None
        self.gps_tow = None
        self.gps_fix = None
        self.gps_numsats = None
        self.gond_batt = None
        self.gond_sta = None
        self.rs41_temp = None
        self.rs41_hum = None
        self.rs41_pres = None
        self.rs41_stat = None
        self.ta1 = None
        self.ti1 = None
        self.ta2 = None
        self.ti2 = None
        self.cw_cp_vr1 = None
        self.cw_cp_vr2 = None
        self.cw_cp_vo1 = None
        self.cw_cp_vo2 = None
        self.cw_cp_cpot = None
        self.cw_cp_gpot = None
        self.gps_veln = None
        self.gps_vele = None
        self.gps_veld = None
        self.hw_cp_vr1 = None
        self.hw_cp_vr2 = None
        self.hw_cp_vo1 = None
        self.hw_cp_vo2 = None
        self.hw_cp_cpot = None
        self.hw_cp_gpot = None
        self.gps_rms_hor = None
        self.gps_rms_ver = None
        self.vent_batt = None
        self.vent_stat = None
        self.vent_ta1 = None
        self.vent_ti1 = None
        self.vent_ta2 = None
        self.vent_ti2 = None
        self.vent_diff = None
        self.gond_batt_c = None
        self.vent_batt_c = None
        self.ta1_c = None
        self.ti1_c = None
        self.ta2_c = None
        self.ti2_c = None
        self.vent_ta1_c = None
        self.vent_ti1_c = None
        self.vent_ta2_c = None
        self.vent_ti2_c = None
        self.gps_veln_c = None
        self.gps_vele_c = None
        self.gps_veld_c = None
        self.converted = None

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
            print('here1')
            if payload['data']['FRAME_TYPE'] == '0xd2a8':
                print('here2')
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
            self.gps_lat = payload['data']['frame_data']['gps_lat']
            self.gps_lon = payload['data']['frame_data']['gps_lon']
            self.gps_alt = payload['data']['frame_data']['gps_alt']
            self.gps_tow = payload['data']['frame_data']['gps_tow']
            self.gps_fix = payload['data']['frame_data']['gps_fix']
            self.gps_numsats = payload['data']['frame_data']['gps_numsats']
            self.gond_batt = payload['data']['frame_data']['GOND_BATT']
            self.gond_sta =  payload['data']['frame_data']['GOND_STA']
            self.rs41_temp =  payload['data']['frame_data']['RS41_Temp']
            self.rs41_hum = payload['data']['frame_data']['RS41_Hum']
            self.rs41_pres = payload['data']['frame_data']['RS41_Pres']
            self.rs41_stat = payload['data']['frame_data']['RS41_Stat']
            self.ta1 = payload['data']['frame_data']['Ta1']
            self.ti1 = payload['data']['frame_data']['Ti1']
            self.ta2 = payload['data']['frame_data']['Ta2']
            self.ti2 = payload['data']['frame_data']['Ti2']
            self.cw_cp_vr1 = payload['data']['frame_data']['CW_CP_Vr1']
            self.cw_cp_vr2 = payload['data']['frame_data']['CW_CP_Vr2']
            self.cw_cp_vo1 = payload['data']['frame_data']['CW_CP_Vo1']
            self.cw_cp_vo2 = payload['data']['frame_data']['CW_CP_Vo2']
            self.cw_cp_cpot = payload['data']['frame_data']['CW_CP_Cpot']
            self.cw_cp_gpot = payload['data']['frame_data']['CW_CP_Gpot']
            self.gps_veln = payload['data']['frame_data']['gps_veln']
            self.gps_vele = payload['data']['frame_data']['gps_vele']
            self.gps_veld = payload['data']['frame_data']['gps_veld']
            self.hw_cp_vr1 = payload['data']['frame_data']['HW_CP_Vr1']
            self.hw_cp_vr2 = payload['data']['frame_data']['HW_CP_Vr2']
            self.hw_cp_vo1 = payload['data']['frame_data']['HW_CP_Vo1']
            self.hw_cp_vo2 = payload['data']['frame_data']['HW_CP_Vo2']
            self.hw_cp_cpot = payload['data']['frame_data']['HW_CP_Cpot']
            self.hw_cp_gpot = payload['data']['frame_data']['HW_CP_Gpot']
            self.gps_rms_hor = payload['data']['frame_data']['gps_rms_hor']
            self.gps_rms_ver = payload['data']['frame_data']['gps_rms_ver']
            self.vent_batt = payload['data']['frame_data']['VENT_BATT']
            self.vent_stat = payload['data']['frame_data']['VENT_STAT']
            self.vent_ta1 = payload['data']['frame_data']['VENT_Ta1']
            self.vent_ti1 = payload['data']['frame_data']['VENT_Ti1']
            self.vent_ta2 = payload['data']['frame_data']['VENT_Ta2']
            self.vent_ti2 = payload['data']['frame_data']['VENT_Ti2']
            self.vent_diff = payload['data']['frame_data']['VENT_DIFF']
            self.gond_batt_c = payload['data']['frame_data']['GOND_BATT_C']
            self.vent_batt_c = payload['data']['frame_data']['VENT_BATT_C']
            self.ta1_c = payload['data']['frame_data']['Ta1_C']
            self.ti1_c = payload['data']['frame_data']['Ti1_C']
            self.ta2_c = payload['data']['frame_data']['Ta2_C']
            self.ti2_c = payload['data']['frame_data']['Ti2_C']
            self.vent_ta1_c = payload['data']['frame_data']['VENT_Ta1_C']
            self.vent_ti1_c = payload['data']['frame_data']['VENT_Ti1_C']
            self.vent_ta2_c = payload['data']['frame_data']['VENT_Ta2_C']
            self.vent_ti2_c = payload['data']['frame_data']['VENT_Ti2_C']
            self.gps_veln_c = payload['data']['frame_data']['gps_veln_C']
            self.gps_vele_c = payload['data']['frame_data']['gps_vele_C']
            self.gps_veld_c = payload['data']['frame_data']['gps_veld_C']
            self.converted = payload['data']['converted']

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
                self.gps_lat,
                self.gps_lon,
                self.gps_alt,
                self.gps_tow,
                self.gps_fix,
                self.gps_numsats,
                self.gond_batt,
                self.gond_sta,
                self.rs41_temp,
                self.rs41_hum,
                self.rs41_pres,
                self.rs41_stat,
                self.ta1,
                self.ti1,
                self.ta2,
                self.ti2,
                self.cw_cp_vr1,
                self.cw_cp_vr2,
                self.cw_cp_vo1,
                self.cw_cp_vo2,
                self.cw_cp_cpot,
                self.cw_cp_gpot,
                self.gps_veln,
                self.gps_vele,
                self.gps_veld,
                self.hw_cp_vr1,
                self.hw_cp_vr2,
                self.hw_cp_vo1,
                self.hw_cp_vo2,
                self.hw_cp_cpot,
                self.hw_cp_gpot,
                self.gps_rms_hor,
                self.gps_rms_ver,
                self.vent_batt,
                self.vent_stat,
                self.vent_ta1,
                self.vent_ti1,
                self.vent_ta2,
                self.vent_ti2,
                self.vent_diff,
                self.gond_batt_c,
                self.vent_batt_c,
                self.ta1_c,
                self.ti1_c,
                self.ta2_c,
                self.ti2_c,
                self.vent_ta1_c,
                self.vent_ti1_c,
                self.vent_ta2_c,
                self.vent_ti2_c,
                self.gps_veln_c,
                self.gps_vele_c,
                self.gps_veld_c,
                self.converted
            )
            
            self.queue.append(self.current_message)

        except Exception as e:
            print("Exception in stat_db_msg func: %s" % e)

    def get_queue(self):
        return self.queue

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
                    await self.write_stat.msg_in(self.queue)

                await asyncio.sleep(0.1)

        except Exception as e:
            print("Exception in MQTT loop: %s" % e)


if __name__ == "__main__":
    mqtt_conn = mqtt_client()
    
    stat_write_loop = write_stat.muri_db_stat()

    loop = asyncio.get_event_loop()

    tasks = [asyncio.ensure_future(mqtt_conn.main_loop())]

    loop.run_until_complete(asyncio.gather(*tasks))
