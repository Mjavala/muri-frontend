# Todo:
-   Doc - https://docs.google.com/document/d/1CSF3hZtkelVOZ4mjL_WDlLTLz2xcdvG2n6zTeEbTXk4/edit?usp=sharing
-   Historical data ui
-   Security config
-   Replication
-   System log files
-   Raw database instance
-   Data ingestion as a service
-   Testing

### Useful Docker commands
-  docker exec -it [img-id] psql -U postgres (connect to postgres)
-  docker-compose start/stop
-  docker inspect [obj]

# DB schema

###   2 relational tables - devices, stations - ||  One time-series hypertable -  device_data
```SQL
CREATE TABLE "devices"(
   device_id   VARCHAR (30),
);

CREATE TABLE "stations"(
   station_id   VARCHAR (30),
);

CREATE TABLE "device_data"(
   time            TIMESTAMP WITH TIME ZONE,
   altitude        REAL,
   rssi            SMALLINT,
   temperature     REAL,
   humidity        REAL,
   device_id       VARCHAR (30),
   station_id      VARCHAR (30)
);

CREATE TABLE "0xd2a8_raw"(
   id             SERIAL PRIMARY KEY,
   station        VARCHAR (20) NOT NULL,
   receiver       VARCHAR (10) NOT NULL,
   timestamp      DOUBLE PRECISION NOT NULL,
   addr_from      VARCHAR (30) NOT NULL,
   rssi_rx        SMALLINT NOT NULL,
   frame_type     VARCHAR (10) NOT NULL,
   frame_cnt      SMALLINT NOT NULL,
   frame          TEXT NOT NULL,
   packet_id      INTEGER NOT NULL,
   packet_num     INTEGER NOT NULL,
   epoch_index    INTEGER NOT NULL,
   gps_lat        REAL NOT NULL,
   gps_lon        REAL NOT NULL,
   gps_alt        REAL NOT NULL,
   gps_tow        INTEGER NOT NULL,
   gps_fix        SMALLINT NOT NULL,
   gps_numsats    SMALLINT NOT NULL,
   batt_mon       SMALLINT NOT NULL,
   gondola_statu  SMALLINT NOT NULL,
   RS41_temp      REAL NOT NULL,
   RS41_hum       REAL NOT NULL,
   RS41_pres      REAL NOT NULL,
   temp_ta1       INTEGER NOT NULL,
   temp_ti1       INTEGER NOT NULL,
   temp_ta2       INTEGER NOT NULL,
   temp_ti2       INTEGER NOT NULL,
   cw_chop_vr1    INTEGER NOT NULL,
   cw_chop_vr2    INTEGER NOT NULL,
   cw_chop_vo1    INTEGER NOT NULL,
   cw_chop_vo2    INTEGER NOT NULL,
   cw_chop_cpot   INTEGER NOT NULL,
   cw_chop_gpot   SMALLINT NOT NULL,
   gps_veln       SMALLINT NOT NULL,
   gps_vele       SMALLINT NOT NULL,
   gps_vel_d      SMALLINT NOT NULL,
   hw_chop_vr1    SMALLINT NOT NULL,
   hw_chop_vr2    SMALLINT NOT NULL,
   hw_chop_vo1    SMALLINT NOT NULL,
   hw_chop_vo2    SMALLINT NOT NULL,
   hw_chop_cpot   SMALLINT NOT NULL,
   hw_chop_gpot   SMALLINT NOT NULL,
   rms_hor_vel    SMALLINT NOT NULL,
   rms_ver_vel    SMALLINT NOT NULL,
   var_35         SMALLINT NOT NULL
);

CREATE TABLE "0xC109_raw"(
   id             SERIAL PRIMARY KEY,
   station        VARCHAR (20) NOT NULL,
   receiver       VARCHAR (10) NOT NULL,
   timestamp      DOUBLE PRECISION NOT NULL,
   addr_from      VARCHAR (30) NOT NULL,
   rssi_rx        SMALLINT NOT NULL,
   frame_type     VARCHAR (10) NOT NULL,
   frame_cnt      SMALLINT NOT NULL,
   frame          TEXT NOT NULL,
   packet_id      INTEGER NOT NULL,
   packet_num     INTEGER NOT NULL,
   epoch_index    INTEGER NOT NULL,
   interval_index SMALLINT NOT NULL,
   gps_lat        REAL NOT NULL,
   gps_lon        REAL NOT NULL,
   gps_alt        REAL NOT NULL,
   gps_tow        INTEGER NOT NULL,
   gps_fix        SMALLINT NOT NULL,
   gps_numsats    SMALLINT NOT NULL,
   cw_sa_0        INTEGER NOT NULL,
   cw_sa_1        INTEGER NOT NULL,
   cw_sa_2        INTEGER NOT NULL,
   cw_sa_3        INTEGER NOT NULL,
   cw_sa_4        INTEGER NOT NULL,
   cw_sa_5        INTEGER NOT NULL,
   cw_sa_6        INTEGER NOT NULL,
   cw_sa_7        INTEGER NOT NULL,
   cw_sa_8        INTEGER NOT NULL,
   hw_sa_0        INTEGER NOT NULL,
   hw_sa_1        INTEGER NOT NULL,
   hw_sa_2        INTEGER NOT NULL,
   hw_sa_3        INTEGER NOT NULL,
   hw_sa_4        INTEGER NOT NULL,
   hw_sa_5        INTEGER NOT NULL,
   hw_sa_6        INTEGER NOT NULL,
   hw_sa_7        INTEGER NOT NULL,
   hw_sa_8        INTEGER NOT NULL,
   cw_meas_vr1    SMALLINT NOT NULL,
   cw_meas_vr2    SMALLINT NOT NULL,
   cw_meas_vo1    SMALLINT NOT NULL,
   cw_meas_vo2    SMALLINT NOT NULL,
   cw_meas_cpot   INTEGER NOT NULL,
   cw_meas_gpot   INTEGER NOT NULL,
   hw_meas_vr1    SMALLINT NOT NULL,
   hw_meas_vr2    SMALLINT NOT NULL,
   hw_meas_vo1    SMALLINT NOT NULL,
   hw_meas_vo2    SMALLINT NOT NULL
);

```
