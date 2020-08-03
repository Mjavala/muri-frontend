import paho.mqtt.client as mosquitto
import json
import time
import asyncio
import stat_db.write_stat as write_stat
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
        self.write_stat = write_stat.muri_db_stat()

        self.mqttc = mosquitto.Client()
        self.mqttc.on_connect = self.on_mqtt_conn
        self.mqttc.on_disconnect = self.on_mqtt_disc
        self.mqttc.on_message = self.on_mqtt_msg

        self.queue = deque()        

        # stat message definition
        self.station = None
        self.stat_time = None
        self.rcvr_last_update = None
        self.period_secs = None
        self.avg_byte_sec = None
        self.tot_bytes = None
        self.par_bytes = None
        self.upr_bytes = None
        self.tot_rad_pkt = None
        self.par_data_pkt = None
        self.upr_data_pkt = None
        self.msg_out_queue = None
        self.rssi = None
        self.secs_ago = None
        self.all = None     # Dynamic JSON, multiple devices possible
        # MQTT Object Fields
        self.mqtt_last_update = None
        self.mqtt_is_up = None
        self.mqtt_qIn = None
        self.mqtt_qOut = None
        self.mqtt_period = None
        self.mqtt_cmd_in = None
        self.mqtt_out = None
        self.mqtt_last_rt = None
        self.mqtt_last_time = None
        self.mqtt_tracks_in_last = None
        self.last_cmd_time = None
        # Tracker Object Fields
        self.tracker_time = None
        self.tracker_gps_lat = None
        self.tracker_gps_lon = None
        self.tracker_gps_alt = None
        self.tracker_gps_fix = None
        self.tracker_gps_numsats = None
        self.tracker_gps_time = None
        self.tracker_gps_tow = None
        self.tracker_gps_veln = None
        self.tracker_gps_vele = None
        self.tracker_gps_veld = None
        # Ant Object Fields
        self.ant_last_update = None
        self.azm = None
        self.elv = None
        self.req_azm = None
        self.req_elv = None
        self.ant_status = None
        self.raw_azm_volts = None
        self.raw_elv_volts = None
        # Track Object Fields
        self.track_last_update = None
        self.track_id = None
        self.track_last_range = None
        self.track_last_azm = None
        self.track_last_elv = None
        self.track_status = None
        self.az_pending = None
        self.el_pending = None
        self.track_last_lat = None
        self.track_last_lon = None
        self.track_last_alt = None
        # Current tracks Object Fields
        self.current_tracks = None  # Dynamic JSON, multiple devices possible

    def on_mqtt_conn(self, client, userdata, flags, rc):
        try:
            if rc == 0:
                self.connected = True
                self.mqttc.subscribe('muri/stat', qos = 2)   # !-- QoS 2 - message received exactly once --!
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
            self.stat_db_data(payload)
            self.stat_db_msg()

    def stat_db_data(self, payload):
        try:
            self.station = payload['station']
            self.stat_time = payload['stat_time']
            self.rcvr_last_update = payload['receiver_1']['last']['last_update']
            self.period_secs = payload['receiver_1']['last']['period_secs']
            self.avg_byte_sec = payload['receiver_1']['last']['avg_byte_sec']
            self.tot_bytes = payload['receiver_1']['last']['tot_bytes']
            self.par_bytes = payload['receiver_1']['last']['par_bytes']
            self.upr_bytes = payload['receiver_1']['last']['upr_bytes']
            self.tot_rad_pkt = payload['receiver_1']['last']['tot_rad_pkt']
            self.par_data_pkt = payload['receiver_1']['last']['par_data_pkt']
            self.upr_data_pkt = payload['receiver_1']['last']['upr_data_pkt']
            self.msg_out_queue = payload['receiver_1']['last']['msg_out_queue']
            self.rssi = payload['receiver_1']['last']['rssi_last']['rssi']
            self.secs_ago = payload['receiver_1']['last']['rssi_last']['secs_ago']
            self.all = payload['receiver_1']['all']
            self.mqtt_last_update = payload['mqtt']['last_update']
            self.mqtt_is_up = payload['mqtt']['isUp']
            self.mqtt_qIn = payload['mqtt']['qIn']
            self.mqtt_qOut = payload['mqtt']['qOut']
            self.mqtt_period = payload['mqtt']['period']
            self.mqtt_cmd_in = payload['mqtt']['cmd_in']
            self.mqtt_out = payload['mqtt']['out']
            self.mqtt_last_rt = payload['mqtt']['last_rt']
            self.mqtt_last_time = payload['mqtt']['last_time']
            self.mqtt_tracks_in_last = payload['mqtt']['tracks_in']['last']
            self.tracker_time = payload['tracker']['time']
            self.tracker_gps_lat = payload['tracker']['gps']['gps_lat']
            self.tracker_gps_lon = payload['tracker']['gps']['gps_lon']
            self.tracker_gps_alt = payload['tracker']['gps']['gps_alt']
            self.tracker_gps_fix = payload['tracker']['gps']['gps_fix']
            self.tracker_gps_numsats = payload['tracker']['gps']['gps_numsats']
            self.tracker_gps_time = payload['tracker']['gps']['gps_time']
            self.tracker_gps_tow = payload['tracker']['gps']['gps_tow']
            self.tracker_gps_veln = payload['tracker']['gps']['gps_veln']
            self.tracker_gps_vele = payload['tracker']['gps']['gps_vele']
            self.tracker_gps_veld = payload['tracker']['gps']['gps_veld']
            self.ant_last_update = payload['tracker']['ant']['last_update']
            self.azm = payload['tracker']['ant']['azm']
            self.elv = payload['tracker']['ant']['elv']
            self.req_azm = payload['tracker']['ant']['req_azm']
            self.req_elv = payload['tracker']['ant']['req_elv']
            self.ant_status = payload['tracker']['ant']['status']
            self.raw_azm_volts = payload['tracker']['ant']['raw_azm_volts']
            self.raw_elv_volts = payload['tracker']['ant']['raw_elv_volts']
            self.track_last_update = payload['tracker']['track']['last_update']
            self.track_id = payload['tracker']['track']['id']
            self.track_last_range = payload['tracker']['track']['last_range']
            self.track_last_azm = payload['tracker']['track']['last_azm']
            self.track_last_elv = payload['tracker']['track']['last_elv']
            self.track_status = payload['tracker']['track']['status']
            self.az_pending = payload['tracker']['track']['az_pending']
            self.el_pending = payload['tracker']['track']['el_pending']
            self.track_last_lat = payload['tracker']['track']['last_lat']
            self.track_last_lon = payload['tracker']['track']['last_lon']
            self.track_last_alt = payload['tracker']['track']['last_alt']
            self.current_tracks = payload['current_tracks']
            self.last_cmd_time = payload['mqtt']['last_cmd_time']

        except Exception as e:
            print('Could not parse object %s' % e)

    def stat_db_msg(self):
        try:
            self.current_message = (
                self.station,
                self.stat_time,
                self.rcvr_last_update,
                self.period_secs,
                self.avg_byte_sec,
                self.tot_bytes,
                self.par_bytes,
                self.upr_bytes,
                self.tot_rad_pkt,
                self.par_data_pkt,
                self.upr_data_pkt,
                self.msg_out_queue,
                self.rssi,
                self.secs_ago,
                self.all,
                self.mqtt_last_update,
                self.mqtt_is_up,
                self.mqtt_qIn,
                self.mqtt_qOut,
                self.mqtt_period,
                self.mqtt_cmd_in,
                self.mqtt_out,
                self.mqtt_last_rt,
                self.mqtt_last_time,
                self.mqtt_tracks_in_last,
                self.tracker_time,
                self.tracker_gps_lat,
                self.tracker_gps_lon,
                self.tracker_gps_alt,
                self.tracker_gps_fix,
                self.tracker_gps_numsats,
                self.tracker_gps_time,
                self.tracker_gps_tow,
                self.tracker_gps_veln,
                self.tracker_gps_vele,
                self.tracker_gps_veld,
                self.ant_last_update,
                self.azm,
                self.elv,
                self.req_azm,
                self.req_elv,
                self.ant_status,
                self.raw_azm_volts,
                self.raw_elv_volts,
                self.track_last_update,
                self.track_id,
                self.track_last_range,
                self.track_last_azm,
                self.track_last_elv,
                self.track_status,
                self.az_pending,
                self.el_pending,
                self.track_last_lat,
                self.track_last_lon,
                self.track_last_alt,
                self.current_tracks,
                self.last_cmd_time
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
