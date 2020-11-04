import asyncio
import time
import json
import mqtt as mqttc
import db as db
import argparse
import os
import logs

LIVE_CHECK_INTERVAL = 10

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

mqtt_conn = mqttc.mqtt_client(MQTT_TOPICS)
db_node = db.muri_db()


async def main_loop():
    last_stat = time.time()
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
            if (time.time() - last_stat > LIVE_CHECK_INTERVAL):
                last_stat = time.time()
                live = mqtt_conn.get_live_flight()
                await asyncio.sleep(0.1)

            if live:
                if not qo.empty():
                    val = qo.get_nowait()
                    db_node.add_to_queue(val)

                if qo.qsize() > 100:
                    await asyncio.sleep(0.3)
                else:
                    await asyncio.sleep(2)
            elif not live:
                db_node.reset_state()

    except Exception as e:
        print(e)

if __name__ == "__main__":

    loop = asyncio.get_event_loop()

    tasks = [
        asyncio.ensure_future(main_loop()),
        asyncio.ensure_future(mqtt_conn.main_loop()),
        asyncio.ensure_future(db_node.main_loop()),
    ]
    loop.run_until_complete(asyncio.gather(*tasks))
