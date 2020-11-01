import asyncio
import logging.handlers as handlers
import time
import json
import mqtt as mqttc
import db as db
import argparse

# STAT_INTERVAL = 1
# LIVE_CHECK_INTERVAL = 5
MQTT_TOPICS = list

parser = argparse.ArgumentParser(description="Live (-r) or simulation (-s) settings")
parser.add_argument("-l", "--live", help="live config", action="store_true")
parser.add_argument("-s", "--sim", help="simulation config", action="store_true")
parser.add_argument("-sdb", "--simdb", help="simulation config", action="store_true")

args = parser.parse_args()

if args.live:
    MQTT_TOPICS = ["live", "muri/raw", "muri/stat"]
elif args.simdb:
    MQTT_TOPICS = ["simdb", "muri_test/raw", "muri_test/stat"]
else:
    MQTT_TOPICS = ["sim", "muri_test/raw", "muri_test/stat"]

mqtt_conn = mqttc.mqtt_client(MQTT_TOPICS)
db_node = db.muri_db()

async def main_loop():

    # queue = mqtt_conn.get_queue()
    while True:
        qo = mqtt_conn.get_q_out()
        qi = mqtt_conn.get_q_in()
        q_db_stat = db_node.get_stat_q()
        q_db_0xc = db_node.get_0xc_q()
        q_db_0xd = db_node.get_0xd_q()

        if not qo.empty():
            val = qo.get_nowait()
            
        print('mqtt in: {} | filtered {} '.format(qi.qsize(), qo.qsize()))

        if not qo.empty():
            val = qo.get_nowait()
            db_node.add_to_queue(val)

        print('stat queue: {} | 0xc queue: {} | 0xd queue: {}'.format(q_db_stat.qsize(), q_db_0xc.qsize(), q_db_0xd.qsize()))

        if qo.qsize() > 100:
            await asyncio.sleep(0.3)
        else:
            await asyncio.sleep(1)


if __name__ == "__main__":
    print("Starting MURI App Main Program")

    loop = asyncio.get_event_loop()

    tasks = [
        asyncio.ensure_future(main_loop()),
        asyncio.ensure_future(mqtt_conn.main_loop()),
        asyncio.ensure_future(db_node.main_loop())
    ]
    loop.run_until_complete(asyncio.gather(*tasks))
