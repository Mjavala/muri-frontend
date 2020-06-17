import asyncio
import asyncpg
import time
import logging
import os
from os.path import join, dirname
from dotenv import load_dotenv
import muri_app_log as muri_app_log

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

USER = os.getenv('DB_USER')
PW = os.getenv('DB_PASSWORD')
DATABASE = os.getenv('DB_NAME')
HOST = os.getenv('DB_HOST')

class muri_db():
    def __init__(self):
        self.current_message = {}
                
        self.last_time = time.time()
        self.id = str
        self.alt = float
        self.rssi = int
        self.temp = float
        self.hum = float 

        self.app_log_setup = muri_app_log.main_app_logs()
        self.logger = logging.getLogger('app')

    async def run(self):
        try:
            self.logger.log_app('--- Writing Data to Database ---')
            print(USER,PW,DATABASE,HOST)
            conn = await asyncpg.connect(user=USER, password=PW, database=DATABASE, host=HOST)
            await conn.execute(
                '''
                    INSERT INTO muri_data VALUES (NOW(), $1, $2, $3, $4, $5)
                ''', self.id, self.alt, self.rssi, self.temp, self.hum)
            await conn.close()

        except Exception as e:
            self.logger.log_app("Exception in Database Connection Script: %s" % e)

    def msg_in(self, payload):
        self.current_message = payload
        print(self.current_message)


    def stat_update(self):
        self.id = self.current_message['mqtt']['device_id']
        self.alt = self.current_message['mqtt']['altitude']
        self.rssi = self.current_message['mqtt']['rssi']
        self.temp = self.current_message['mqtt']['temperature']
        self.hum = self.current_message['mqtt']['humidity']

    def initialConditionChecks(self, message):
        if message == {} or message == None:
            return False
        if message['humidity'] == float or message['temperature'] == float:
            return False
        return True

    async def main_loop(self):
        last_time = time.time()
        self.logger.log_app('--- Database service started succesfully ---')
        try:
            while(True):
                if (time.time() - last_time > 5): 
                    last_time = time.time()
                    message = self.current_message.get('mqtt', None)
                    
                    if (self.initialConditionChecks(message)):
                        self.stat_update()
                        await self.run()

                await asyncio.sleep(0.1)
        except Exception as e:
            self.logger.log_app("Exception in Database Service: %s" % e)


if __name__ == "__main__":
    db_conn =  muri_db()

    loop = asyncio.get_event_loop()

    loop.run_until_complete(asyncio.ensure_future(db_conn.main_loop()))