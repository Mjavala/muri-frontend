#!/usr/bin/python3

# Muri App Main Program
# Program Structure: 
#   - muri_app_main (runs async, mult instances allowed)
#   - muri_app_mqtt (runs async, sgl instance)
#   - muri_db (sgl instance, single operation (R/W) connection to DB)
#   - muri_app_log (sgl instance, needs to be configured for your directory structure)
#   - Muri App Main Program (muri_app_main)
#       - Async. Runs logging, MQTT and Database service. Watchdog. General Logging

import asyncio
import logging
import logging.handlers as handlers
import time
import json
import muri_app_mqtt as mqttc
import muri_db as muri_db
import muri_db_raw as muri_db_raw
import muri_app_log as muri_app_log

STAT_INTERVAL = 5

mqtt_conn = mqttc.muri_app_mqtt()
db = muri_db.muri_db()
db_raw = muri_db_raw.muri_db_raw()

async def main_loop(): 

    last_stat = time.time()
    logger = logging.getLogger('app')

    while (True):

        try: 

            if (time.time() - last_stat > STAT_INTERVAL): 
                last_stat = time.time() 
                #stat_msg = {"mqtt": mqtt_conn.get_stats()}
                raw_msg = mqtt_conn.get_raw_msg()
                # stat msg to database
                #db.msg_in(stat_msg)
                db_raw.msg_in(raw_msg)

                #logger.log_app(json.dumps(stat_msg))
            await asyncio.sleep(0.01)
        
        except Exception as e: 
            logger.log_app("Main Loop Exception: %s" % e)



if __name__ == '__main__':
    muri_app_log.main_app_logs()
    muri_app_log.db_logs()
    logger = logging.getLogger('app')


    logger.log_app("Starting MURI App Main Program")

    loop = asyncio.get_event_loop()

    tasks = [asyncio.ensure_future(main_loop()),
             asyncio.ensure_future(mqtt_conn.main_loop()),
             asyncio.ensure_future(db.main_loop()),
             asyncio.ensure_future(db_raw.main_loop())]

    loop.run_until_complete(asyncio.gather(*tasks))
