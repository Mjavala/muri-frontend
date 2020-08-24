import asyncio
import asyncpg
import time
import logging
import os
from os.path import join, dirname
from dotenv import load_dotenv
import db_log

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

USER = os.getenv('DB_USER')
PW = os.getenv('DB_PASSWORD')
DATABASE = os.getenv('DB_NAME')
HOST = os.getenv('DB_HOST')

class muri_db():
    def __init__(self):
        self.client_pool = None

        self.logger = logging.getLogger('db')

        self.current_payload = []
        self.device_id = None
        self.station_id = None

    async def write_db(self):
        try:
            self.logger.log_app('--- Writing Data to Database ---')
            conn = await self.client_pool.acquire()
            await conn.execute(
                '''
                INSERT INTO "DEVICES"(addr) VALUES ($1) ON CONFLICT DO NOTHING
                ''', self.device_id
                )

            await conn.execute(
                '''
                INSERT INTO "STATIONS"(stat_addr) VALUES ($1) ON CONFLICT DO NOTHING
                ''', self.station_id
                )
            await conn.copy_records_to_table(
                'device_data', records=self.current_payload,
                columns=[
                    'data_time', 'device_id', 'station_id', 'latitude', 'longitude', 
                    'altitude', 'rssi', 'temperature', 'batt_mon', 'vent_batt', 'packet_type',
                    'packet_id', 'temp_amb_1', 'temp_int_1', 'temp_int_2', 'gps_tow'
                ])

        except Exception as e:
            self.logger.log_app("Exception in Database Connection Script: %s" % e)

        finally:
            await self.client_pool.release(conn)

    async def msg_in(self, payload):
        self.current_payload = payload

        result = self.initialConditionChecks(self.current_payload)
        
        if result:
        #   Multple balloons logic, must check each bucket for different ID/StationID fields
            self.device_id = self.current_payload[1][1]
            self.station_id = self.current_payload[2][2]
            await self.write_db()

    def initialConditionChecks(self, message):
        if message == {}:
            return False

        if message == None:
            return False

        return True

    async def main_loop(self):
        last_time = time.time()
        self.logger.log_app('--- Database service started succesfully ---')
        try:
            self.client_pool = await asyncpg.create_pool(host=HOST, user=USER, password=PW)
            self.logger.log_app('--- Database client pool started succesfully ---')
            while(True):
                # need to make this reactive to self.current_message instead of at 5 sec intervals
                if (time.time() - last_time > 5): 
                    last_time = time.time()
                    
                    #if (self.initialConditionChecks(message)):
                        #self.stat_update()
                        #await self.write_db()

                await asyncio.sleep(1)
        except Exception as e:
            self.logger.log_app("Exception in Database Service: %s" % e)


if __name__ == "__main__":
    db_conn =  muri_db()

    loop = asyncio.get_event_loop()

    loop.run_until_complete(asyncio.ensure_future(db_conn.main_loop()))