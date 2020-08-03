import asyncio
import asyncpg
import time
import logging
import os
from os.path import join, dirname
from dotenv import load_dotenv
import traceback

dotenv_path = join(dirname(__file__), '../../.env')
load_dotenv(dotenv_path)

USER = os.getenv('DB_USER')
PW = os.getenv('DB_PASSWORD')
DATABASE = os.getenv('DB_NAME')
#   Note diff host from muri_db
HOST = os.getenv('DB_HOST')


class db_0xc109():
    def __init__(self):
        self.current_message = {}
        self.message_type = str

        self.client_pool = None

        self.queue = None

        #self.app_log_setup = muri_app_log.main_app_logs()
        #self.logger = logging.getLogger('db')
    async def write_stat_db(self, payload):
        try:
            #print('--- Writing Data to 0xc109 Msg Database ---')
            conn = await self.client_pool.acquire()

            await conn.execute(
                '''
                INSERT INTO "inc_0xc109" (
                    station,
                    receiver,
                    date_rcv,
                    addr_from,
                    rssi,
                    frame_type,
                    frame_cnt,
                    frame,
                    packet_id,
                    packet_num,
                    epoch_index,
                    interval_index,
                    gps_lat,
                    gps_lon,
                    gps_alt,
                    gps_tow,
                    gps_fix, 
                    gps_numsats, 
                    cw_sa_0,
                    cw_sa_1, 
                    cw_sa_2, 
                    cw_sa_3,
                    cw_sa_4, 
                    cw_sa_5, 
                    cw_sa_6,
                    cw_sa_7,
                    cw_sa_8,
                    hw_sa_0, 
                    hw_sa_1,
                    hw_sa_2, 
                    hw_sa_3, 
                    hw_sa_4,
                    hw_sa_5, 
                    hw_sa_6, 
                    hw_sa_7,
                    hw_sa_8,
                    cw_vr1,
                    cw_vr2, 
                    cw_vo1, 
                    cw_vo2,
                    cw_cpot, 
                    cw_gpot, 
                    hw_vr1, 
                    hw_vr2, 
                    hw_vo1,
                    hw_vo2
                    ) VALUES(
                    $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15,
                    $16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28,
                    $29, $30, $31, $32, $33, $34, $35, $36, $37, $38, $39, $40, $41,
                    $42, $43, $44, $45, $46)
                ''', 
                payload[0], payload[1], payload[2], payload[3], payload[4], payload[5], payload[6],
                payload[7], payload[8], payload[9], payload[10], payload[11], payload[12], payload[13],
                payload[14], payload[15], payload[16], payload[17], payload[18], payload[19], payload[20],
                payload[21], payload[22], payload[23], payload[24], payload[25], payload[26], payload[27], payload[28],
                payload[29], payload[30], payload[31], payload[32], payload[33], payload[34], payload[35],
                payload[36], payload[37], payload[38], payload[39], payload[40], payload[41], payload[42], payload[43],
                payload[44], payload[45]
            )

        except Exception as e:
            print("Exception in Database Connection Script: %s" % e)
            traceback.print_exc()

        finally:
            await self.client_pool.release(conn)

    # entrypoint for incoming stat msgs
    async def msg_in(self, queue):
        self.queue = queue

        await asyncio.sleep(0.1)

    def queue_state(self):
        if self.queue != None:
            if len(self.queue) == 0:
                return False, None
            else:
                result = self.queue.popleft()
                return True, result
        return None, None

    async def main_loop(self):
        last_time = time.time()
        try:
            self.client_pool = await asyncpg.create_pool(host=HOST, user=USER, password=PW, database=DATABASE)
            while(True):
                if (time.time() - last_time > 1):
                    result, payload = self.queue_state()
                    if result:
                        print(len(payload))
                        await self.write_stat_db(payload)

                    last_time = time.time()
                await asyncio.sleep(0.1)

        except Exception as e:
            print("Exception in stat database service: %s" % e)
            traceback.print_exc()


if __name__ == "__main__":
    db_conn =  muri_db_stat()

    loop = asyncio.get_event_loop()

    loop.run_until_complete(asyncio.ensure_future(db_conn.main_loop()))