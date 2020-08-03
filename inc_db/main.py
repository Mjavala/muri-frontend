#!/usr/bin/python3

# Muri App Main Program
# TODO: - refactor mqtt client and asyncpg pool connection

import asyncio
import logging
import logging.handlers as handlers
import time
import json
import stat_db.mqtt_client as mqttc
import stat_db.write_stat as db_stat
import raw_db_0xc109.mqtt_client as mqttc_0xc
import raw_db_0xc109.write_db_0xc as db_0xc109
import raw_db_0xd2a8.mqtt_client as mqttc_0xd
import raw_db_0xd2a8.write_db_0xd as db_0xd2a8


STAT_INTERVAL = 1

mqtt_conn = mqttc.stat_client()
db = db_stat.muri_db_stat()

mqtt_con_0xc = mqttc_0xc.mqtt_0xc()
db_0xc = db_0xc109.db_0xc109()

mqtt_con_0xd = mqttc_0xd.mqtt_0xd()
db_0xd = db_0xd2a8.db_0xd2a8()

async def main_loop():

    last_stat = time.time()

    while (True):
        try: 
            if (time.time() - last_stat > STAT_INTERVAL): 
                last_stat = time.time()
                # stat client
                result = mqtt_conn.get_queue()
                await db.msg_in(result)
                # 0xc109 client
                result_0xc = mqtt_con_0xc.get_queue()
                await db_0xc.msg_in(result_0xc)
                # 0xd2a8 client
                result_0xd = mqtt_con_0xd.get_queue()
                await db_0xd.msg_in(result_0xd)

            await asyncio.sleep(0.1)
            
        except Exception as e:
            print("Main Loop Exception: %s" % e)
    await asyncio.sleep(0.1)



if __name__ == '__main__':

    loop = asyncio.get_event_loop()

    tasks = [asyncio.ensure_future(main_loop()),
             asyncio.ensure_future(mqtt_conn.main_loop()),
             asyncio.ensure_future(mqtt_con_0xc.main_loop()),
             asyncio.ensure_future(mqtt_con_0xd.main_loop()),
             asyncio.ensure_future(db_0xc.main_loop()),
             asyncio.ensure_future(db_0xc.main_loop()),
             asyncio.ensure_future(db_0xd.main_loop())]

    loop.run_until_complete(asyncio.gather(*tasks))
