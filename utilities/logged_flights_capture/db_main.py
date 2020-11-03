# This clone of the main program is a tool to send older data files over MQTT.
# It is intended as a temporary standalone solution decoupled from the muri database service, and must be run manually.
# The purpose of this program is to capture old data, or data that couldn't be captured at the time, in the postgres database.
# This will be deprecated in future versions in favor of a bulk insert approach.

import asyncio
import logging
import logging.handlers as handlers
import time
import json
import db_mqtt as mqttc
import muri_db as muri_db


STAT_INTERVAL = 1
STAT_INTERVAL_LIVE = 5

mqtt_conn = mqttc.muri_app_mqtt()
#db = muri_db.muri_db()

async def main_loop():

    last_stat = time.time()
    live = False

    while (True):
        if (time.time() - last_stat > STAT_INTERVAL_LIVE):
            last_stat = time.time()
            live = mqtt_conn.live_flight()
            await asyncio.sleep(0.1)
        if live:
            try: 
                if (time.time() - last_stat > STAT_INTERVAL): 
                    last_stat = time.time()
                    result = mqtt_conn.bucket_to_db()
                    if (result):
                        #await db.msg_in(result)
                        print(result)
                await asyncio.sleep(0.5)
                
            except Exception as e:
                print("Main Loop Exception: %s" % e)
        await asyncio.sleep(0.1)



if __name__ == '__main__':

    loop = asyncio.get_event_loop()

    tasks = [asyncio.ensure_future(main_loop()),
             asyncio.ensure_future(mqtt_conn.main_loop())]
             #asyncio.ensure_future(db.main_loop())]

    loop.run_until_complete(asyncio.gather(*tasks))
