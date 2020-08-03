import asyncio
import asyncpg
import time
import logging
import os
from os.path import join, dirname
from dotenv import load_dotenv
import traceback
#import muri_app_log as muri_app_log

dotenv_path = join(dirname(__file__), '../../.env')
load_dotenv(dotenv_path)

USER = os.getenv('DB_USER')
PW = os.getenv('DB_PASSWORD')
DATABASE = os.getenv('DB_NAME')
#   Note diff host from muri_db
HOST = os.getenv('DB_HOST')


class db_0xd2a8():
    def __init__(self):
        self.current_message = {}
        self.message_type = str

        self.client_pool = None

        self.queue = None

        #self.app_log_setup = muri_app_log.main_app_logs()
        #self.logger = logging.getLogger('db')
    async def write_stat_db(self, payload):
        try:
            conn = await self.client_pool.acquire()
            print('--- Writing to 0xd2a8 DB ---')
            await conn.execute(
                '''
                INSERT INTO "inc_0xd2a8" (
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
                    gps_lat,
                    gps_lon,
                    gps_alt,
                    gps_tow,
                    gps_fix, 
                    gps_numsats, 
                    gond_batt,
                    gond_sta, 
                    rs41_temp, 
                    rs41_hum,
                    rs41_pres, 
                    rs41_stat, 
                    ta1,
                    ti1,
                    ta2, 
                    ti2,
                    cw_cp_vr1, 
                    cw_cp_vr2, 
                    cw_cp_vo1,
                    cw_cp_vo2, 
                    cw_cp_cpot, 
                    cw_cp_gpot,
                    gps_veln, 
                    gps_vele, 
                    gps_veld,
                    hw_cp_vr1, 
                    hw_cp_vr2, 
                    hw_cp_vo1, 
                    hw_cp_vo2, 
                    hw_cp_cpot,
                    hw_cp_gpot, 
                    gps_rms_hor, 
                    gps_rms_ver,
                    vent_batt, 
                    vent_stat, 
                    vent_ta1,
                    vent_ti1, 
                    vent_ta2, 
                    vent_ti2,
                    vent_diff, 
                    gond_batt_c, 
                    vent_batt_c,
                    ta1_c, 
                    ti1_c, 
                    ta2_c,
                    ti2_c,
                    vent_ta1_c,
                    vent_ti1_c,
                    vent_ta2_c,
                    vent_ti2_c,
                    gps_veln_c,
                    gps_vele_c,
                    gps_veld_c,
                    converted
                    ) VALUES(
                    $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15,
                    $16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28,
                    $29, $30, $31, $32, $33, $34, $35, $36, $37, $38, $39, $40, $41,
                    $42, $43, $44, $45, $46, $47, $48, $49, $50, $51, $52, $53, $54,
                    $55, $56, $57, $58, $59, $60, $61, $62, $63, $64, $65)
                ''', 
                payload[0], payload[1], payload[2], payload[3], payload[4], payload[5], payload[6],
                payload[7], payload[8], payload[9], payload[10], payload[11], payload[12], payload[13],
                payload[14], payload[15], payload[16], payload[17], payload[18], payload[19], payload[20],
                payload[21], payload[22], payload[23], payload[24], payload[25], payload[26], payload[27], payload[28],
                payload[29], payload[30], payload[31], payload[32], payload[33], payload[34], payload[35],
                payload[36], payload[37], payload[38], payload[39], payload[40], payload[41], payload[42], payload[43],
                payload[44], payload[45], payload[46], payload[47], payload[48], payload[49], payload[50], payload[51],
                payload[52], payload[53], payload[54], payload[55], payload[56], payload[57], payload[58], payload[59],
                payload[60], payload[61], payload[62], payload[63], payload[64]
            )

        except Exception as e:
            print("Exception in Database Connection Script: %s" % e)
            traceback.print_exc()

        finally:
            await self.client_pool.release(conn)

    # entrypoint for incoming stat msgs
    async def msg_in(self, queue, pool):
        self.client_pool = pool
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
        print('--- starting 0xd2a8 message loop ---')
        last_time = time.time()
        try:
            while(True):
                if (time.time() - last_time > 1):
                    result, payload = self.queue_state()
                    if result:
                        if self.client_pool != None:
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