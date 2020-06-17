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
#   Note diff host from muri_db
HOST = os.getenv('DB_HOST_RAW')

class muri_db_raw():
    def __init__(self):
        self.current_message = {}
        self.message_type = str

        self.app_log_setup = muri_app_log.main_app_logs()
        self.logger = logging.getLogger('db')

    async def run_0xd2a8(self):
        try: 
            self.logger.info('--- Writing Data to Raw database (0xd2a8) ---')
            conn = await asyncpg.connect(user=USER, password=PW, database=DATABASE, host=HOST)
            query = '''
                        INSERT INTO "0xd2a8_raw"
                            (
                                station,
                                receiver,
                                timestamp,
                                addr_from,
                                rssi_rx,
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
                                batt_mon,
                                gondola_statu,
                                RS41_temp,
                                RS41_hum,
                                RS41_pres,
                                temp_ta1,
                                temp_ti1,
                                temp_ta2,
                                temp_ti2,
                                cw_chop_vr1,
                                cw_chop_vr2,
                                cw_chop_vo1,
                                cw_chop_vo2,
                                cw_chop_cpot,
                                cw_chop_gpot,
                                gps_veln,
                                gps_vele,
                                gps_vel_d,
                                hw_chop_vr1,
                                hw_chop_vr2,
                                hw_chop_vo1,
                                hw_chop_vo2,
                                hw_chop_cpot,
                                hw_chop_gpot,
                                rms_hor_vel,
                                rms_ver_vel,
                                var_35
                            ) 
                            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, 
                            $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, 
                            $21, $22, $23, $24, $25, $26, $27, $28, $29, $30,
                            $31, $32, $33, $34, $35, $36, $37, $38, $39, $40, $41, $42, $43)
                    '''
            values = self.stat_update_0xd2a8()

            await conn.execute(query, *values)

            await conn.close()

        except Exception as e:
            self.logger.log_app("Exception in Database (0xd2a8) Connection Script: %s" % e)

    async def run_0xc109(self):
        try: 
            self.logger.log_app('--- Writing Data to Raw database (0xc109) ---')
            conn = await asyncpg.connect(user=USER, password=PW, database=DATABASE, host=HOST)
            query = '''
                        INSERT INTO "0xC109_raw" (
                            
                        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15,
                    $16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28, $29, $30,
                    $31, $32, $33, $34, $35, $36, $37, $38, $39, $40, $41, $42, $43, $44, $45, $46)
                    '''
            values = self.stat_update_0xc109()

            await conn.execute(query, *values)

            await conn.close()

        except Exception as e:
            self.logger.log_app("Exception in Database (0xc109) Connection Script: %s" % e)

    def msg_in(self, payload):
        self.current_message = payload
        self.message_type = payload['data']['FRAME_TYPE']


    def stat_update_0xc109(self):
        try:
            msg_obj = [
                self.current_message['station'],
                self.current_message['receiver'],
                self.current_message['data']['TIMESTAMP'],
                self.current_message['data']['ADDR_FROM'],
                self.current_message['data']['RSSI_RX'],
                self.current_message['data']['FRAME_TYPE'],
                self.current_message['data']['FRAME_CNT'],
                self.current_message['data']['FRAME'],
                self.current_message['data']['frame_data']['packet_id'],
                self.current_message['data']['frame_data']['packet_num'],
                self.current_message['data']['frame_data']['epoch index'],
                self.current_message['data']['frame_data']['interval index'],
                self.current_message['data']['frame_data']['gps_lat'],
                self.current_message['data']['frame_data']['gps_lon'],
                self.current_message['data']['frame_data']['gps_alt'],
                self.current_message['data']['frame_data']['gps_tow'],
                self.current_message['data']['frame_data']['gps_fix'],
                self.current_message['data']['frame_data']['gps_numsats'],
                self.current_message['data']['frame_data']['CW SA 0'],
                self.current_message['data']['frame_data']['CW SA 1'],
                self.current_message['data']['frame_data']['CW SA 2'],
                self.current_message['data']['frame_data']['CW SA 3'],
                self.current_message['data']['frame_data']['CW SA 4'],
                self.current_message['data']['frame_data']['CW SA 5'],
                self.current_message['data']['frame_data']['CW SA 6'],
                self.current_message['data']['frame_data']['CW SA 7'],
                self.current_message['data']['frame_data']['CW SA 8'],
                self.current_message['data']['frame_data']['HW SA 0'],
                self.current_message['data']['frame_data']['HW SA 1'],
                self.current_message['data']['frame_data']['HW SA 2'],
                self.current_message['data']['frame_data']['HW SA 3'],
                self.current_message['data']['frame_data']['HW SA 4'],
                self.current_message['data']['frame_data']['HW SA 5'],
                self.current_message['data']['frame_data']['HW SA 6'],
                self.current_message['data']['frame_data']['HW SA 7'],
                self.current_message['data']['frame_data']['HW SA 8'],
                self.current_message['data']['frame_data']['CW Meas Vr1'],
                self.current_message['data']['frame_data']['CWMeas Vr2'],
                self.current_message['data']['frame_data']['CW Meas Vo1'],
                self.current_message['data']['frame_data']['CWMeas Vo2'],
                self.current_message['data']['frame_data']['CW Meas Cpot'],
                self.current_message['data']['frame_data']['CW Meas Gpot'],
                self.current_message['data']['frame_data']['HW Meas Vr1'],
                self.current_message['data']['frame_data']['HW Meas Vr2'],
                self.current_message['data']['frame_data']['HW Meas Vo1'],
                self.current_message['data']['frame_data']['HW Meas Vo2']
            ]
            print(len(msg_obj))
        except Exception as e:
            self.logger.log_app("Exception in parsing 0xc109 message field: %s" % e)

        return msg_obj


    def stat_update_0xd2a8(self):
        try:
            msg_obj = [
                self.current_message['station'],
                self.current_message['receiver'],
                self.current_message['data']['TIMESTAMP'],
                self.current_message['data']['ADDR_FROM'],
                self.current_message['data']['RSSI_RX'],
                self.current_message['data']['FRAME_TYPE'],
                self.current_message['data']['FRAME_CNT'],
                self.current_message['data']['FRAME'],
                self.current_message['data']['frame_data']['packet_id'],
                self.current_message['data']['frame_data']['packet_num'],
                self.current_message['data']['frame_data']['epoch index'],
                self.current_message['data']['frame_data']['gps_lat'],
                self.current_message['data']['frame_data']['gps_lon'],
                self.current_message['data']['frame_data']['gps_alt'],
                self.current_message['data']['frame_data']['gps_tow'],
                self.current_message['data']['frame_data']['gps_fix'],
                self.current_message['data']['frame_data']['gps_numsats'],
                self.current_message['data']['frame_data']['Batt Mon'],
                self.current_message['data']['frame_data']['Gondola Statu'],
                self.current_message['data']['frame_data']['RS41 Temp'],
                self.current_message['data']['frame_data']['RS41 Hum'],
                self.current_message['data']['frame_data']['RS41 Pres'],
                self.current_message['data']['frame_data']['temp Ta1 (amb)'],
                self.current_message['data']['frame_data']['temp Ti1 (int)'],
                self.current_message['data']['frame_data']['temp Ta2 (amb)'],
                self.current_message['data']['frame_data']['temp Ti2 (int)'],
                self.current_message['data']['frame_data']['CW Chop Vr1'],
                self.current_message['data']['frame_data']['CW Chop Vr2'],
                self.current_message['data']['frame_data']['CW Chop Vo1'],
                self.current_message['data']['frame_data']['CW Chop Vo2'],
                self.current_message['data']['frame_data']['CW Chop Cpot'],
                self.current_message['data']['frame_data']['CW Chop Gpot'],
                self.current_message['data']['frame_data']['gps_veln'],
                self.current_message['data']['frame_data']['gps_vele'],
                self.current_message['data']['frame_data']['gps_vel_d'],
                self.current_message['data']['frame_data']['HW Chop Vr1'],
                self.current_message['data']['frame_data']['HW Chop Vr2'],
                self.current_message['data']['frame_data']['HW Chop Vo1'],
                self.current_message['data']['frame_data']['HW Chop Vo2'],
                self.current_message['data']['frame_data']['HW Chop Cpot'],
                self.current_message['data']['frame_data']['HW Chop Gpot'],
                self.current_message['data']['frame_data']['RMS Hor Vel'],
                self.current_message['data']['frame_data']['RMS Ver Vel'],
                self.current_message['data']['frame_data']['var_35']
            ]
            print(len(msg_obj))
        except Exception as e:
            self.logger.log_app("Exception in parsing 0xc109 message field: %s" % e)

        return msg_obj

    async def main_loop(self):
        last_time = time.time()
        self.logger.log_app('--- Raw database service started succesfully ---')
        try:
            while(True):
                if (time.time() - last_time > 5): 
                    last_time = time.time()

                    if self.message_type == '0xd2a8':

                        await self.run_0xd2a8()
                        continue

                    if self.message_type == '0xc109':

                        await self.run_0xc109()
                        continue
                    else:
                        pass


                await asyncio.sleep(0.1)

        except Exception as e:
            self.logger.log_app("Exception in raw database service: %s" % e)


if __name__ == "__main__":
    db_conn =  muri_db_raw()

    loop = asyncio.get_event_loop()

    loop.run_until_complete(asyncio.ensure_future(db_conn.main_loop()))