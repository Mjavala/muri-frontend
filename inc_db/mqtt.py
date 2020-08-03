import paho.mqtt.client as mosquitto
import json
import time
import asyncio
import os
from os.path import join, dirname
from dotenv import load_dotenv
import stat_db.mqtt_client as stat_msg
import stat_db.write_stat as write_stat

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

MQTT_USER = os.getenv('MQTT_USER')
MQTT_PASS = os.getenv('MQTT_PASS')
MQTT_HOST = os.getenv('MQTT_HOST')

class mqtt_client():

    def __init__(self): 
        #self.app_log_setup = db_log.main_app_logs()
        #self.logger = logging.getLogger('app')
        
        self.current_message = None

        self.mqttc = mosquitto.Client()
        self.mqttc.on_connect = self.on_mqtt_conn
        self.mqttc.on_disconnect = self.on_mqtt_disc
        self.mqttc.on_message = self.on_mqtt_msg

        self.stat_msg_instance = stat_msg.stat_client()

    def on_mqtt_conn(self, client, userdata, flags, rc):
        try:
            if rc == 0:
                self.connected = True
                self.mqttc.subscribe('muri/raw', qos = 2)   # !-- QoS 2 - message received exactly once --!
                self.mqttc.subscribe('muri/stat', qos = 2)   # !-- QoS 2 - message received exactly once --!
                print("!!! MQTT Client Connected! !!!")
                print("--- MQTT Subscribed to muri/raw ---")
                print("--- MQTT Subscribed to muri/stat ---")
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
        print(message.topic)
        payload = json.loads(str(message.payload.decode()))
        
        if message.topic == 'muri/raw':
            if payload['data']['FRAME_TYPE'] == '0xd2a8':
                # 0xd2a8 entrypoint
                pass
            if payload['data']['FRAME_TYPE'] == '0xc109':
                # 0xc109 entrypoint
                pass

        if message.topic == 'muri/stat':
            # stat entrypoint
            try:
                self.stat_msg_instance.stat_db_data(payload)
            except Exception as e:
                print('Error decoding stat message %s' % e)
            

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
                if (time.time() - last_time > 60):
                    print('--- MQTT Client live ---')
                    last_time = time.time()

                await asyncio.sleep(0.1)

        except Exception as e:
            print("Exception in MQTT loop: %s" % e)


if __name__ == "__main__":
    mqtt_conn = mqtt_client()
    stat_loop = stat_msg.stat_client()
    write_loop = write_stat.muri_db_stat()
    
    loop = asyncio.get_event_loop()

    tasks = [asyncio.ensure_future(mqtt_conn.main_loop())]

    loop.run_until_complete(asyncio.gather(*tasks))
