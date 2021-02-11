'''
Program Entrypoint
Nodes
    -   main_loop ~ Master node (Watchdog)
    -   mqtt_loop ~ Data ingestion node
    -   db_loop ~ Data write node

Configuration
    -   Live ~ default, no CLI argument. This will listen to MQTT data from 'muri/raw' and 'muri/stat'; and write data.
    -   -sdb --simdb ~ Listens to MQTT data from 'muri_test/raw' and 'muri_test/stat' and writes data.
    -   -s --sim ~ Listens to MQTT data from 'muri_test/raw' and 'muri_test/stat', does not write data.
    -   Logging directory created on startup at /root/muri/

'''

import asyncio
import time
import json
import mqtt as mqttc
import db as db
import argparse
import os
import logs
import traceback

# Config / Logging dir setup
path = os.path.join(os.path.expanduser("~"), "muri")

parser = argparse.ArgumentParser(
    description="Live (no args) simulation (-sdb / -s) settings"
)
# parser.add_argument("-l", "--live", help="live config", action="store_true")
parser.add_argument("-s", "--sim", help="simulation config", action="store_true")
parser.add_argument("-sdb", "--simdb", help="simulation config", action="store_true")

args = parser.parse_args()

if args.simdb:
    MQTT_TOPICS = ["simdb", "muri_test/raw", "muri_test/stat"]
elif args.sim:
    MQTT_TOPICS = ["sim", "muri_test/raw", "muri_test/stat"]
else:
    MQTT_TOPICS = ["live", "muri/raw", "muri/stat"]

print(MQTT_TOPICS)
mqtt_conn = mqttc.mqtt_client(MQTT_TOPICS)
db_node = db.muri_db()


async def main_loop():
    live = False
    
    try:
        logger = logs.main_app_logs()
        logger.info("Starting MURI App Main Program...")

        if not os.path.exists(path):
            os.mkdir(path)
            logger.info("Logging directory made")

        logger.info("Starting MURI database service...")

        qo = mqtt_conn.get_q_out()

        while True:
            live = mqtt_conn.get_live_flight()

            if live:
                logger.info("Getting filtered message from filtered queue... | Size: {}".format(qo.qsize()))
                if not qo.empty():
                    val = qo.get_nowait()
                    db_node.add_to_queue(val)

                if qo.qsize() > 100:
                    await asyncio.sleep(0.3)
                else:
                    await asyncio.sleep(2)
            elif not live:
                if not qo.empty():
                    logger.info("Flight Ended. Items still in MQTT Filtered Queue: {}".format(qo.qsize()))
                await asyncio.sleep(5)

    except Exception as e:
        traceback.print_exc(e)

if __name__ == "__main__":

    loop = asyncio.get_event_loop()

    tasks = [
        asyncio.ensure_future(main_loop()),
        asyncio.ensure_future(mqtt_conn.main_loop()),
        asyncio.ensure_future(db_node.main_loop()),
    ]
    loop.run_until_complete(asyncio.gather(*tasks))
