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
HOST = os.getenv('DB_HOST')


class muri_db_stat():
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

            await conn.execute(
                '''
                INSERT INTO "stat_msgs" (
                    station,
                    stat_time,
                    rcvr_last_update,
                    period_secs,
                    avg_byte_sec,
                    tot_bytes,
                    par_bytes,
                    upr_bytes,
                    tot_rad_pkt,
                    par_data_pkt,
                    upr_data_pkt,
                    msg_out_queue,
                    rssi,
                    secs_ago,
                    all_devices,
                    mqtt_last_update, 
                    mqtt_is_up, 
                    mqtt_qin,
                    mqtt_qout, 
                    mqtt_period, 
                    mqtt_cmd_in,
                    mqtt_out, 
                    mqtt_last_rt, 
                    mqtt_last_time,
                    tracks_last_in,
                    tracker_time, 
                    tracker_gps_lat,
                    tracker_gps_lon, 
                    tracker_gps_alt, 
                    tracker_gps_fix,
                    tracker_gps_numsats, 
                    tracker_gps_time, 
                    tracker_gps_tow,
                    tracker_gps_veln, 
                    tracker_gps_vele, 
                    tracker_gps_veld,
                    ant_last_update, 
                    azm, 
                    elv, 
                    req_azm, 
                    req_elv,
                    ant_status, 
                    raw_azm_volts, 
                    raw_elv_volts,
                    track_last_update, 
                    track_id, 
                    track_last_range,
                    track_last_azm, 
                    track_last_elv, 
                    track_status,
                    az_pending, 
                    el_pending, 
                    track_last_lat,
                    track_last_lon, 
                    track_last_alt, 
                    current_tracks,
                    last_cmd_in
                    ) VALUES(
                    $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15,
                    $16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28,
                    $29, $30, $31, $32, $33, $34, $35, $36, $37, $38, $39, $40, $41,
                    $42, $43, $44, $45, $46, $47, $48, $49, $50, $51, $52, $53, $54,
                    $55, $56, $57)
                ''', 
                payload[0], payload[1], payload[2], payload[3], payload[4], payload[5], payload[6],
                payload[7], payload[8], payload[9], payload[10], payload[11], payload[12], payload[13],
                str(payload[14]), payload[15], payload[16], payload[17], payload[18], payload[19], payload[20],
                payload[21], payload[22], payload[23], payload[24], payload[25], payload[26], payload[27], payload[28],
                payload[29], payload[30], payload[31], payload[32], payload[33], payload[34], payload[35],
                payload[36], payload[37], payload[38], payload[39], payload[40], payload[41], payload[42], payload[43],
                payload[44], payload[45], payload[46], payload[47], payload[48], payload[49], payload[50], payload[51],
                payload[52], payload[53], payload[54], str(payload[55]), payload[56]
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
        try:
            if self.queue != None:
                if len(self.queue) == 0:
                    return False, None
                else:
                    result = self.queue.popleft()
                    return True, result
            return None, None
        except Exception as e:
            print('!!! queue state exception !!! %s' % e)

    async def main_loop(self):
        last_time = time.time()
        try:
            self.client_pool = await asyncpg.create_pool(host=HOST, user=USER, password=PW, database=DATABASE)
            while(True):
                if (time.time() - last_time > 1):
                    result, payload = self.queue_state()
                    if result:
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