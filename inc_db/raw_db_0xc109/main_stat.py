#!/usr/bin/python3

# Muri App Main Program
# Program Structure: 
#   - db_main (runs async, mult instances allowed)
#   - db_mqtt (runs async, sgl instance)
#   - muri_db (sgl instance, single operation (R/W) connection to DB)
#   - db_log (sgl instance, needs to be configured for your directory structure)
#   - Muri App Main Program (db_main)
#       - Async. Runs logging, MQTT and Database service. Watchdog. General Logging

import asyncio
import logging
import logging.handlers as handlers
import time
import json
import mqtt_client as mqttc
import write_stat as db_stat

STAT_INTERVAL = 1

mqtt_conn = mqttc.mqtt_client()
db = db_stat.muri_db_stat()

async def main_loop():

    last_stat = time.time()

    while (True):
        try: 
            if (time.time() - last_stat > STAT_INTERVAL): 
                last_stat = time.time()
                result = mqtt_conn.get_queue()
                await db.msg_in(result)

            await asyncio.sleep(0.1)
            
        except Exception as e:
            print("Main Loop Exception: %s" % e)
    await asyncio.sleep(0.1)



if __name__ == '__main__':

    loop = asyncio.get_event_loop()

    tasks = [asyncio.ensure_future(main_loop()),
             asyncio.ensure_future(mqtt_conn.main_loop()),
             asyncio.ensure_future(db.main_loop())]

    loop.run_until_complete(asyncio.gather(*tasks))
