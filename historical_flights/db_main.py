#!/usr/bin/python3

# Muri App Main Program
# Program Structure: 
#   - db_main (runs async, sgl instance)
#   - db_mqtt (runs async, sgl instance)
#   - muri_db (sgl instance, single operation (R/W) connection to DB)
#   - db_log (sgl instance, outputs app/db logs at current directory. Logs rotate hourly.)

import asyncio
import logging
import logging.handlers as handlers
import time
import json
import db_mqtt as mqttc
import muri_db as muri_db
import db_log as muri_db_log

STAT_INTERVAL = 1
LIVE_CHECK_INTERVAL = 5

mqtt_conn = mqttc.muri_app_mqtt()
db = muri_db.muri_db()

async def main_loop():

    last_stat = time.time()
    logger = logging.getLogger('app')
    live = False

    while (True):
        if (time.time() - last_stat > LIVE_CHECK_INTERVAL):
            last_stat = time.time()
            # DGRS stations output stat messages every ~ 30 seconds regardless of whether there is a live flight or not.
            live = mqtt_conn.live_flight()
            await asyncio.sleep(0.1)
        if live:
            try: 
                if (time.time() - last_stat > STAT_INTERVAL): 
                    last_stat = time.time()
                    result = mqtt_conn.bucket_to_db()
                    if (result):
                        await db.msg_in(result)
                await asyncio.sleep(0.5)
                
            except Exception as e:
                logger.log_app("Main Loop Exception: %s" % e)
        await asyncio.sleep(0.1)



if __name__ == '__main__':
    muri_db_log.main_app_logs()
    muri_db_log.db_logs()
    logger = logging.getLogger('app')


    logger.log_app("Starting MURI App Main Program")

    loop = asyncio.get_event_loop()

    tasks = [asyncio.ensure_future(main_loop()),
             asyncio.ensure_future(mqtt_conn.main_loop()),
             asyncio.ensure_future(db.main_loop())]

    loop.run_until_complete(asyncio.gather(*tasks))
