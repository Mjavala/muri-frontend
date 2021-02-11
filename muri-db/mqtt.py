'''
Live Flight Conditions:
    -   muri/raw channel ~ data must come from a VALID balloon payload.
    -   GPS must be locked ( 3 > ).
    -   Live flight tracker (flight_live) object must be False.

This node provides a lot of useful log information:
    -   Total MQTT messages received on a live flight, seperated by topic (raw/stat)
    -   Total valid message count in the MQTT ingestion Queue (q_in)
    -   Total filtered messagecount in the MQTT Output Queue (q_out)
    -   Notifications on live flight detection

The threshold for a live flight to be done is a full minute without seeing a device payload. 
Once a flight is done, the state is reset and this node begins to once again listen for live flights.
Messages still in the queue at this point will still be processed by the main and db nodes.
'''
import paho.mqtt.client as mosquitto
import json
import time
import asyncio
import os
from os.path import join, dirname
from dotenv import load_dotenv
import filter_messages
import logs

dotenv_path = join(
    dirname(__file__), "/root/muri/.env"
)  # depends on your directory structure
load_dotenv(dotenv_path)

MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASS = os.getenv("MQTT_PASS")
MQTT_HOST = os.getenv("MQTT_HOST")


class mqtt_client:
    def __init__(self, topics):
        self.q_in = asyncio.Queue()
        self.q_out = asyncio.Queue()
        self.filter = filter_messages.filter_mqtt()

        self.tracker = time.time()

        self.mqttc = mosquitto.Client(
            client_id="{}-{}".format("DB_CLIENT", time.time()), clean_session=True
        )
        self.mqtt_config = topics
        # MQTT Callbacks
        self.mqttc.on_connect = self.on_mqtt_conn
        self.mqttc.on_disconnect = self.on_mqtt_disc
        self.mqttc.on_message = self.on_mqtt_msg
        self.payload = {"destination": str, "message": dict, "device": str}
        # Live balloon hook
        self.flight_live = False
        self.live_device = None

        # message counts
        self.stat_count = 0
        self.raw_count = 0

        self.logger = logs.main_app_logs()
        self.mqtt_msg_count = 0

    def on_mqtt_conn(self, client, userdata, flags, rc):
        if rc == 0:
            topics = self.mqtt_subscribe()
            try:
                self.mqttc.subscribe(
                    topics["raw"], qos=2
                )  # !-- QoS 2 - message received exactly once --!
                self.mqttc.subscribe(
                    topics["stat"], qos=2
                )  # !-- QoS 2 - message received exactly once --!
            except Exception as e:
                self.logger.warn("!!! ERROR Subscring to Topics: {} !!!".format(e))
            self.logger.info("--- MQTT Connected! ---")
            self.logger.info(
                "subscribed to: {} , {}".format(topics["raw"], topics["stat"])
            )
        else:
            self.logger.info("!!! MQTT Connection Failed! !!!")

    def on_mqtt_disc(self, client, userdata, rc):
        if rc != 0:
            self.logger.warn("!!! MQTT Disconnceted Unexpectedly !!!")
        else:
            self.logger.info("!!! MQTT Disconnceted Planned !!!")

    def on_mqtt_msg(self, client, userdata, message):
        self.mqtt_msg_count += 1
        self.payload["message"] = json.loads(str(message.payload.decode()))

        # live flight check
        if self.mqtt_config[0] == "live":
            # gps locked | check telemetry data is transmitting & package is not corrupted
            if message.topic == "muri/raw":
                if self.payload["message"]["data"]:
                    if self.payload["message"]["data"]["frame_data"]:
                        if self.payload["message"]["data"]["frame_data"]["gps_fix"] >= 3 and self.flight_live == False:
                            self.logger.info("!!! Live Flight Detected !!!")
                            self.flight_live = True

        if self.flight_live:
            if message.topic == "muri/raw":
                self.payload["destination"] = self.payload["message"]["data"][
                    "FRAME_TYPE"
                ]
                self.tracker = time.time()
                self.payload["device"] = self.payload["message"]["data"]["ADDR_FROM"]
                self.live_device = self.payload["message"]["data"]["ADDR_FROM"]
                self.raw_count += 1
                self.q_in.put_nowait(self.payload)
            elif message.topic == "muri/stat" and self.live_device is not None:
                self.payload["destination"] = "stat"

                if self.payload["message"]["station"] != "VGRS1":
                    self.stat_count += 1
                    self.q_in.put_nowait(self.payload)

        # simulation config for test channels
        elif self.mqtt_config[0] == "simdb":
            # will pass here in production
            try:
                if message.topic == "muri_test/raw":
                    if self.payload["message"]["data"]["frame_data"]:

                        self.payload["destination"] = self.payload["message"]["data"][
                            "FRAME_TYPE"
                        ]
                        self.raw_count += 1
                        self.tracker = time.time()
                        self.payload["device"] = self.payload["message"]["data"][
                            "ADDR_FROM"
                        ]
                        self.live_device = self.payload["message"]["data"]["ADDR_FROM"]
                        self.q_in.put_nowait(self.payload)
                elif message.topic == "muri_test/stat" and self.live_device is not None:
                    self.payload["destination"] = "stat"

                    # TEST01 station sim only
                    if self.payload["message"]["station"] != "VTST1":
                        self.stat_count += 1
                        self.q_in.put_nowait(self.payload)
            except Exception as e:
                self.logger.info(e)

        elif self.mqtt_config[0] == "sim":
            pass

    def mqtt_subscribe(self):
        self.logger.info("MQTT Config: {}".format(self.mqtt_config))
        return {"raw": self.mqtt_config[1], "stat": self.mqtt_config[2]}

    async def start_mqtt(self):

        try:
            self.mqttc.username_pw_set(MQTT_USER, MQTT_PASS)

            self.logger.info("Connecting to MQTT Server....")
            self.mqttc.connect_async(MQTT_HOST, 8883, keepalive=15)
            self.mqttc.loop_start()

        except Exception as e:
            self.logger.warn("Exception in MQTT Start Script: %s" % e)

    def get_q_out(self):
        return self.q_out

    def get_q_in(self):
        return self.q_in

    def get_live_flight(self):
        return self.flight_live

    async def main_loop(self):
        self.logger.info("Starting MQTT Main Loop...")
        try:
            await self.start_mqtt()
            self.logger.info("Initial Config: Live flight: {} | Tracker: {}...".format(self.flight_live, self.tracker))
            while True:
                if self.flight_live:
                    self.logger.info("MQTT Stats: Live device: {} | Qsizes (raw:stat): {}:{} ".format(self.live_device, self.raw_count, self.stat_count))
                    self.logger.info("MQTT Queues: Qin: {} | Qout: {} ".format(self.q_in.qsize(), self.q_out.qsize()))
                    # if a xbee payload has not been received in 1 mins, assume the flight has ended.
                    if time.time() - self.tracker > 60:
                        self.logger.info("5 minutes since any live payload received from {}, Flight ended. Listening ...".format(self.live_device))
                        self.flight_live = False
                        self.live_device = None

                    if not self.q_in.empty():
                        payload = self.q_in.get_nowait()
                        result = self.filter.new(payload)
                        self.q_out.put_nowait(result)

                    if self.q_in.qsize() > 100:
                        await asyncio.sleep(0.2)
                    else:
                        self.logger.info("Current Status:: Live Flight: {} | Live Device: {}".format(self.flight_live, self.live_device))
                        self.logger.info("MQTT Ingestion Status:: Raw Msg: {} | Stat Msg: {} | Totals: {}".format(self.raw_count, self.stat_count, self.mqtt_msg_count))
                        self.logger.info("MQTT Queues:: Qin: {} | Qout: {}".format(self.q_in.qsize(), self.q_out.qsize()))
                        await asyncio.sleep(1)
                elif not self.flight_live:
                    await asyncio.sleep(5)
        except Exception as e:
            self.logger.warn("Exception in MQTT Main Loop: %s" % e)
        finally:
            pass


if __name__ == "__main__":
    mqtt_conn = mqtt_client(["live", "muri/raw", "muri/stat"])

    loop = asyncio.get_event_loop()

    loop.run_until_complete(asyncio.ensure_future(mqtt_conn.main_loop()))
