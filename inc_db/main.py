#!/usr/bin/python3
# TODO: - refactor mqtt client and asyncpg pool connection
import asyncio
import asyncpg
import logging
import logging.handlers as handlers
import time
import json
import os
import mqtt as mqttc
import stat_db.write_stat as db_stat
import raw_db_0xc109.write_db_0xc as db_0xc109
import raw_db_0xd2a8.write_db_0xd as db_0xd2a8

from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

USER = os.getenv('DB_USER')
PW = os.getenv('DB_PASSWORD')
DATABASE = os.getenv('DB_NAME')
HOST = os.getenv('DB_HOST')

STAT_INTERVAL = 1

mqtt_conn = mqttc.stat_client()

db = db_stat.muri_db_stat()
db_0xc = db_0xc109.db_0xc109()
db_0xd = db_0xd2a8.db_0xd2a8()

async def main_loop():
    client_pool = await asyncpg.create_pool(host=HOST, user=USER, password=PW, database=DATABASE)
    last_stat = time.time()
    while (True):
        try:
            if (time.time() - last_stat > STAT_INTERVAL): 
                last_stat = time.time()
                # stat client
                result = mqtt_conn.get_queue_stat()
                await db.msg_in(result, client_pool)
                # 0xc109 client
                result_0xc = mqtt_conn.get_queue_0xc109()
                await db_0xc.msg_in(result_0xc, client_pool)
                # 0xd2a8 client
                result_0xd = mqtt_conn.get_queue_0xd2a8()
                await db_0xd.msg_in(result_0xd, client_pool)

            await asyncio.sleep(0.1)
            
        except Exception as e:
            print("Main Loop Exception: %s" % e)
    await asyncio.sleep(0.1)



if __name__ == '__main__':

    loop = asyncio.get_event_loop()

    tasks = [asyncio.ensure_future(main_loop()),
             asyncio.ensure_future(mqtt_conn.main_loop()),
             asyncio.ensure_future(db.main_loop()),
             asyncio.ensure_future(db_0xc.main_loop()),
             asyncio.ensure_future(db_0xd.main_loop())]

    loop.run_until_complete(asyncio.gather(*tasks))
