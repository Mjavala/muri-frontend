import asyncio
import asyncpg
import time
import logging
import os
from os.path import join, dirname
from dotenv import load_dotenv
import db_log
from re import search
import traceback


dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

USER = os.getenv('DB_USER')
PW = os.getenv('DB_PASSWORD')
DATABASE = os.getenv('DB_NAME')
HOST = os.getenv('DB_HOST')

class muri_db():
    def __init__(self):
        self.client_pool = None
        self.devices = []
        self.device_dates = []
        self.rows_to_delete = []

        self.first_record = None
        self.last_record =  None

    async def get_device_list(self):
        try:
            conn = await self.client_pool.acquire()
            values = await conn.fetch('''select "addr" from "DEVICES" ''')
            for i in values:
                self.devices.append(i[0])

        except Exception as e:
            print("Exception in Database Connection Script: %s" % e)

        finally:
            await self.client_pool.release(conn)

    async def get_device_dates(self, device):
        try:
            conn = await self.client_pool.acquire()
            values = await conn.fetch('select "id", "data_time" from "device_data" where "device_id" = $1', device)
            self.device_dates = dict(values)

        except Exception as e:
            print("Exception in Database Connection Script: %s" % e)

        finally:
            await self.client_pool.release(conn)

    def filter_dates(self, dates):
        substring = '2020'
        for key, date in dates.items():
            if not search(substring, date):
                self.rows_to_delete.append(key)

    async def filter_for_year(self):
        await self.get_device_list()
        for i in range(len(self.devices)):
            await self.get_device_dates(self.devices[i])
            self.filter_dates(self.device_dates)
        
        print(self.rows_to_delete)

                

    async def main_loop(self):
        last_time = time.time()
        print('--- Database service started succesfully ---')
        try:
            self.client_pool = await asyncpg.create_pool(host=HOST, user=USER, password=PW)
            print('--- Database client pool started succesfully ---')
            print('--- Getting list of known devices ---')
            await self.filter_for_year()

            while(True):
                # need to make this reactive to self.current_message instead of at 5 sec intervals
                if (time.time() - last_time > 5):
                    
                    #if (self.initialConditionChecks(message)):
                        #self.stat_update()
                        #await self.write_db()

                    await asyncio.sleep(1)
        except Exception as e:
            print("Exception in Database Service: %s" % e)
            traceback.print_exc()


if __name__ == "__main__":
    db_conn =  muri_db()

    loop = asyncio.get_event_loop()

    loop.run_until_complete(asyncio.ensure_future(db_conn.main_loop()))