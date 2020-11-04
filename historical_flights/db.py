import asyncio
from os.path import join, dirname
from dotenv import load_dotenv
import os
import asyncpg
import traceback
import logs

dotenv_path = join(dirname(__file__), "/root/muri/.env")
load_dotenv(dotenv_path)

USER = os.getenv("DB_USER")
PW = os.getenv("DB_PASSWORD")
DATABASE = os.getenv("DB_NAME")
HOST = os.getenv("DB_HOST")


class muri_db:
    def __init__(self):
        self.client_pool = None

        self.q_stat = asyncio.Queue()
        self.q_0xc = asyncio.Queue()
        self.q_0xd = asyncio.Queue()

        self.write_stat_counter = 0
        self.write_0xc_counter = 0
        self.write_0xd_counter = 0

        self.logger = logs.main_app_logs()

    def get_stat_q(self):
        return self.q_stat

    def get_0xc_q(self):
        return self.q_0xc

    def get_0xd_q(self):
        return self.q_0xd

    def add_to_queue(self, payload):
        if payload is not None:
            try:
                if payload["topic"] == "stat":
                    self.q_stat.put_nowait(payload["message"])
                elif payload["topic"] == "0xc109":
                    self.q_0xc.put_nowait(payload["message"])
                elif payload["topic"] == "0xd2a8":
                    self.q_0xd.put_nowait(payload["message"])
            except Exception as e:
                self.logger.warn("DB Queues ERROR: {}".format(e))
                self.logger.info("DB Payload: {}".format(payload))

    def sender(self, q):
        while True:
            n = q.qsize()
            batch = []
            # Note that we to put a limit on the whole batch collection process,
            # so we put the loop inside move_on_after
            while len(batch) < n:
                batch.append(q.get_nowait())

            return batch

    def reset_state(self):
        self.logger.info("Resetting Database service to default state...")
        self.write_stat_counter = 0
        self.write_0xc_counter = 0
        self.write_0xd_counter = 0

    async def write_stat(self, payload):
        try:
            async with self.client_pool.acquire() as con:
                if self.write_stat_counter == 0:
                    await con.execute(
                        """
                        INSERT INTO "DEVICES"(addr) VALUES ($1) ON CONFLICT DO NOTHING
                        """,
                        payload[0][4],
                    )

                    await con.execute(
                        """
                        INSERT INTO "STATIONS"(stat_addr) VALUES ($1) ON CONFLICT DO NOTHING
                        """,
                        payload[0][1],
                    )
                    self.write_stat_counter += 1
                await con.copy_records_to_table(
                    "device_data",
                    records=payload,
                    columns=["data_time", "station_id", "rssi", "slant", "device_id"],
                )
                print("--- Writing stat data to db ---")
        except Exception as e:
            self.logger.error(e, exc_info=True)

    async def write_0xc109(self, payload):
        try:
            async with self.client_pool.acquire() as con:
                if self.write_0xc_counter == 0:
                    await con.execute(
                        """
                        INSERT INTO "DEVICES"(addr) VALUES ($1) ON CONFLICT DO NOTHING
                        """,
                        payload[0][2],
                    )

                    await con.execute(
                        """
                        INSERT INTO "STATIONS"(stat_addr) VALUES ($1) ON CONFLICT DO NOTHING
                        """,
                        payload[0][0],
                    )
                    self.write_0xc_counter += 1
                await con.copy_records_to_table(
                    "device_data",
                    records=payload,
                    columns=[
                        "station_id",
                        "data_time",
                        "device_id",
                        "packet_type",
                        "frame",
                        "latitude",
                        "longitude",
                        "altitude",
                        "packet_id",
                        "gps_tow",
                        "hw_vo1",
                        "hw_vo2",
                        "cw_vo1",
                        "cw_vo2",
                    ],
                )
                print("--- Writing 0xc109 data to db ---")
        except Exception as e:
            self.logger.error(e, exc_info=True)

    async def write_0xd2a8(self, payload):
        try:
            async with self.client_pool.acquire() as con:
                if self.write_0xd_counter == 0:
                    await con.execute(
                        """
                        INSERT INTO "DEVICES"(addr) VALUES ($1) ON CONFLICT DO NOTHING
                        """,
                        payload[0][2],
                    )

                    await con.execute(
                        """
                        INSERT INTO "STATIONS"(stat_addr) VALUES ($1) ON CONFLICT DO NOTHING
                        """,
                        payload[0][0],
                    )
                    self.write_0xd_counter += 1
                await con.copy_records_to_table(
                    "device_data",
                    records=payload,
                    columns=[
                        "station_id",
                        "data_time",
                        "device_id",
                        "packet_type",
                        "frame",
                        "latitude",
                        "longitude",
                        "altitude",
                        "packet_id",
                        "gps_tow",
                        "batt_mon",
                        "vent_batt",
                        "temp_amb_1",
                        "temperature",
                        "temp_int_1",
                        "temp_int_2",
                    ],
                )
                print("--- Writing 0xd2a8 data to db ---")
        except Exception as e:
            self.logger.error(e, exc_info=True)

    async def main_loop(self):
        self.logger.info("Starting DB Main Loop...")
        try:
            self.client_pool = await asyncpg.create_pool(
                host=HOST, user=USER, password=PW
            )
        except Exception as e:
            self.logger.error(e, exc_info=True)

        while True:
            # Necessary to satisfy foreign constraints in current DB architecture
            if (
                self.write_stat_counter > 0
                or self.write_0xc_counter > 0
                or self.write_0xd_counter > 0
            ):
                self.write_0xc_counter += 1
                self.write_0xd_counter += 1
                self.write_stat_counter += 1

            # print('stat queue: {} | 0xc queue: {} | 0xd queue: {}'.format(self.q_stat.qsize(), self.q_0xc.qsize(), self.q_0xd.qsize()))

            if not self.q_stat.empty():
                self.logger.info("DB Queue | stat size: {} ".format(self.q_stat.qsize()))
                try:
                    batch = self.sender(self.q_stat)
                    await self.write_stat(batch)
                except Exception as e:
                    self.logger.error(e, exc_info=True)
            if not self.q_0xc.empty():
                self.logger.info("DB Queue | 0xc109 size: {} ".format(self.q_0xc.qsize()))
                try:
                    batch = self.sender(self.q_0xc)
                    await self.write_0xc109(batch)
                except Exception as e:
                    self.logger.error(e, exc_info=True)
            if not self.q_0xd.empty():
                self.logger.info("DB Queue | 0xd2a8 size: {}".format(self.q_0xd.qsize()))
                try:
                    batch = self.sender(self.q_0xd)
                    await self.write_0xd2a8(batch)
                except Exception as e:
                    self.logger.error(e, exc_info=True)

            await asyncio.sleep(10)


if __name__ == "__main__":
    db_conn = muri_db()

    loop = asyncio.get_event_loop()

    loop.run_until_complete(asyncio.ensure_future(db_conn.main_loop()))
