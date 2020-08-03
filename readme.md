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
   date_rcv      DOUBLE PRECISION NOT NULL,
   addr_from      VARCHAR (50) NOT NULL,
   rssi		      SMALLINT NOT NULL,
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
   gond_batt      SMALLINT NOT NULL,
   gond_sta  	  SMALLINT NOT NULL,
   rs41_temp      REAL NOT NULL,
   rs41_hum       REAL NOT NULL,
   rs41_pres      REAL NOT NULL,
   rs41_stat	  REAL NOT NULL,
   ta1       	  REAL NOT NULL,
   ti1       	  REAL NOT NULL,
   ta2       	  REAL NOT NULL,
   ti2       	  REAL NOT NULL,
   cw_cp_vr1      INTEGER NOT NULL,
   cw_cp_vr2	  INTEGER NOT NULL,
   cw_cp_vo1      INTEGER NOT NULL,
   cw_cp_vo2      INTEGER NOT NULL,
   cw_cp_cpot     INTEGER NOT NULL,
   cw_cp_gpot     INTEGER NOT NULL,
   gps_veln       SMALLINT NOT NULL,
   gps_vele       SMALLINT NOT NULL,
   gps_veld       SMALLINT NOT NULL,
   hw_cp_vr1      INTEGER NOT NULL,
   hw_cp_vr2      INTEGER NOT NULL,
   hw_cp_vo1      INTEGER NOT NULL,
   hw_cp_vo2      INTEGER NOT NULL,
   hw_cp_cpot     INTEGER NOT NULL,
   hw_cp_gpot     INTEGER NOT NULL,
   gps_rms_hor    SMALLINT NOT NULL,
   gps_rms_ver    SMALLINT NOT NULL,
   vent_batt      SMALLINT NOT NULL,
   vent_stat	  SMALLINT NOT NULL,
   vent_ta1		  INTEGER NOT NULL,
   vent_ti1		  INTEGER NOT NULL,
   vent_ta2		  INTEGER NOT NULL,
   vent_ti2       INTEGER NOT NULL,
   vent_diff	  INTEGER NOT NULL,
   gond_batt_c    DOUBLE PRECISION NOT NULL,
   vent_batt_c    DOUBLE PRECISION NOT NULL,
   ta1_c		  DOUBLE PRECISION NOT NULL,
   ti1_c		  DOUBLE PRECISION NOT NULL,
   ta2_c	      DOUBLE PRECISION NOT NULL,
   ti2_c		  DOUBLE PRECISION NOT NULL,
   vent_ta1_c	  DOUBLE PRECISION NOT NULL,
   vent_ti1_c	  DOUBLE PRECISION NOT NULL,
   vent_ta2_c     DOUBLE PRECISION NOT NULL,
   vent_ti2_c     DOUBLE PRECISION NOT NULL,
   gps_veln_c	  REAL NOT NULL,
   gps_vele_c	  REAL NOT NULL,
   gps_veld_c	  REAL NOT NULL,
   converted	  DOUBLE PRECISION NOT NULL,
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
