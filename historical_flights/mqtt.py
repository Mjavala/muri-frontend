import paho.mqtt.client as mosquitto
import json
import time
import asyncio
import os
from os.path import join, dirname
from dotenv import load_dotenv
import filter_messages

dotenv_path = join(dirname(__file__), ".env")  # depends on your directory structure
load_dotenv(dotenv_path)

MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASS = os.getenv("MQTT_PASS")
MQTT_HOST = os.getenv("MQTT_HOST")


class mqtt_client:
    def __init__(self, topics):
        self.q_in = asyncio.Queue()
        self.q_out = asyncio.Queue()
        self.filter = mqtt_filter = filter_messages.filter_mqtt()

        self.tracker = time.time()

        self.mqttc = mosquitto.Client(
            client_id="{}-{}".format("DB_CLIENT", time.time()), clean_session=True
        )
        self.mqtt_config = topics
        # MQTT Callbacks
        self.mqttc.on_connect = self.on_mqtt_conn
        self.mqttc.on_disconnect = self.on_mqtt_disc
        self.mqttc.on_message = self.on_mqtt_msg
        self.payload = {"destination": str, "message": dict}
        # Live balloon hook
        self.flight_live = False
        self.mqtt_live = False

    def is_live(self):
        return self.live

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
                print(e)
            self.mqtt_live = True
            print("--- MQTT Connected! ---")
            print("subscribed to: %s , %s" % topics.raw, topics.stat)
        else:
            print("!!! MQTT Connection Failed! !!!")

    def on_mqtt_disc(self, client, userdata, rc):
        self.mqtt_live = False
        if rc != 0:
            print("!!! MQTT Disconnceted Unexpectedly !!!")
        else:
            print("!!! MQTT Disconnceted Planned !!!")

    def on_mqtt_msg(self, client, userdata, message):
        self.payload["message"] = json.loads(str(message.payload.decode()))

        # live flight check
        if self.mqtt_config[0] == "live":
            # gps locked | check telemetry data is transmitting & package is not corrupted
            if (
                message.topic == "muri/raw"
                and (self.payload["message"]["data"]["frame_data"])
                and (self.payload["message"]["data"]["frame_data"]["gps_fix"] >= 3)
                and (self.flight_live == False)
            ):
                self.flight_live = True

        if self.flight_live:
            if message.topic == "muri/raw":
                self.payload["destination"] = self.payload["message"]["data"][
                    "FRAME_TYPE"
                ]
                self.tracker = time.time()
            elif message.topic == "muri/stat":
                self.payload["destination"] = "stat"

            self.q_in.put_nowait(self.payload)

        # simulation config for test channels
        elif self.mqtt_config[0] == "simdb":
            # will pass here in production
            try:
                if message.topic == "muri_test/raw":

                    self.payload["destination"] = self.payload["message"]["data"][
                        "FRAME_TYPE"
                    ]
                    self.tracker = time.time()
                elif message.topic == "muri_test/stat":
                    self.payload["destination"] = "stat"

                # TEST01 station sim only
                if self.payload["message"]["station"] != "VTST1":
                    self.q_in.put_nowait(self.payload)
            except Exception as e:
                print(e)

        elif self.mqtt_config[0] == "sim":
            pass

    def mqtt_subscribe(self):
        print("MQTT Config: {}".format(self.mqtt_config))
        return {"raw": self.mqtt_config[1], "stat": self.mqtt_config[2]}

    async def start_mqtt(self):

        try:
            self.mqttc.username_pw_set(MQTT_USER, MQTT_PASS)

            print("Connecting to MQTT Server....")
            self.mqttc.connect_async(MQTT_HOST, 8883, keepalive=15)
            self.mqttc.loop_start()

        except Exception as e:
            print("Exception in MQTT Start Script: %s" % e)

    def get_q_out(self):
        return self.q_out

    def get_q_in(self):
        return self.q_in

    async def main_loop(self):
        try:
            await self.start_mqtt()
            while True:
                try:
                    # if a xbee payload has not been received in 5 mins, assume the flight has ended.
                    if time.time() - self.tracker > 300 and self.flight_live:
                        self.flight_live = False

                    if not self.q_in.empty():
                        payload = self.q_in.get_nowait()
                        result = self.filter.new(payload)
                        self.q_out.put_nowait(result)

                except Exception as e:
                    print(e)

                if self.q_in.qsize() > 100:
                    await asyncio.sleep(0.2)
                else:
                    await asyncio.sleep(0.5)
        except Exception as e:
            print("Exception in MQTT: %s" % e)
        finally:
            pass


if __name__ == "__main__":
    mqtt_conn = mqtt_client(["muri/raw", "muri/stat"])

    loop = asyncio.get_event_loop()

    loop.run_until_complete(asyncio.ensure_future(mqtt_conn.main_loop()))
