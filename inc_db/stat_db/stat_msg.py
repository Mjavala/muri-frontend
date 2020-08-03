def decode(self, payload):
    try:
        self.station = payload['station']
        self.stat_time = payload['stat_time']
        self.rcvr_last_update = payload['receiver_1']['last']['last_update']
        self.period_secs = payload['receiver_1']['last']['period_secs']
        self.avg_byte_sec = payload['receiver_1']['last']['avg_byte_sec']
        self.tot_bytes = payload['receiver_1']['last']['tot_bytes']
        self.par_bytes = payload['receiver_1']['last']['par_bytes']
        self.upr_bytes = payload['receiver_1']['last']['upr_bytes']
        self.tot_rad_pkt = payload['receiver_1']['last']['tot_rad_pkt']
        self.par_data_pkt = payload['receiver_1']['last']['par_data_pkt']
        self.upr_data_pkt = payload['receiver_1']['last']['upr_data_pkt']
        self.msg_out_queue = payload['receiver_1']['last']['msg_out_queue']
        self.rssi = payload['receiver_1']['last']['rssi_last']['rssi']
        self.secs_ago = payload['receiver_1']['last']['rssi_last']['secs_ago']
        self.all = payload['receiver_1']['all']
        self.mqtt_last_update = payload['mqtt']['last_update']
        self.mqtt_is_up = payload['mqtt']['isUp']
        self.mqtt_qIn = payload['mqtt']['qIn']
        self.mqtt_qOut = payload['mqtt']['qOut']
        self.mqtt_period = payload['mqtt']['period']
        self.mqtt_cmd_in = payload['mqtt']['cmd_in']
        self.mqtt_out = payload['mqtt']['out']
        self.mqtt_last_rt = payload['mqtt']['last_rt']
        self.mqtt_last_time = payload['mqtt']['last_time']
        self.mqtt_tracks_in_last = payload['mqtt']['tracks_in']['last']
        self.tracker_time = payload['tracker']['time']
        self.tracker_gps_lat = payload['tracker']['gps']['gps_lat']
        self.tracker_gps_lon = payload['tracker']['gps']['gps_lon']
        self.tracker_gps_alt = payload['tracker']['gps']['gps_alt']
        self.tracker_gps_fix = payload['tracker']['gps']['gps_fix']
        self.tracker_gps_numsats = payload['tracker']['gps']['gps_numsats']
        self.tracker_gps_time = payload['tracker']['gps']['gps_time']
        self.tracker_gps_tow = payload['tracker']['gps']['gps_tow']
        self.tracker_gps_veln = payload['tracker']['gps']['gps_veln']
        self.tracker_gps_vele = payload['tracker']['gps']['gps_vele']
        self.tracker_gps_veld = payload['tracker']['gps']['gps_veld']
        self.ant_last_update = payload['tracker']['ant']['last_update']
        self.azm = payload['tracker']['ant']['azm']
        self.elv = payload['tracker']['ant']['elv']
        self.req_azm = payload['tracker']['ant']['req_azm']
        self.req_elv = payload['tracker']['ant']['req_elv']
        self.ant_status = payload['tracker']['ant']['status']
        self.raw_azm_volts = payload['tracker']['ant']['raw_azm_volts']
        self.raw_elv_volts = payload['tracker']['ant']['raw_elv_volts']
        self.track_last_update = payload['tracker']['track']['last_update']
        self.track_id = payload['tracker']['track']['id']
        self.track_last_range = payload['tracker']['track']['last_range']
        self.track_last_azm = payload['tracker']['track']['last_azm']
        self.track_last_elv = payload['tracker']['track']['last_elv']
        self.track_status = payload['tracker']['track']['status']
        self.az_pending = payload['tracker']['track']['az_pending']
        self.el_pending = payload['tracker']['track']['el_pending']
        self.track_last_lat = payload['tracker']['track']['last_lat']
        self.track_last_lon = payload['tracker']['track']['last_lon']
        self.track_last_alt = payload['tracker']['track']['last_alt']
        self.current_tracks = payload['current_tracks']
        self.last_cmd_time = payload['mqtt']['last_cmd_time']

        current_message = (
            self.station,
            self.stat_time,
            self.rcvr_last_update,
            self.period_secs,
            self.avg_byte_sec,
            self.tot_bytes,
            self.par_bytes,
            self.upr_bytes,
            self.tot_rad_pkt,
            self.par_data_pkt,
            self.upr_data_pkt,
            self.msg_out_queue,
            self.rssi,
            self.secs_ago,
            self.all,
            self.mqtt_last_update,
            self.mqtt_is_up,
            self.mqtt_qIn,
            self.mqtt_qOut,
            self.mqtt_period,
            self.mqtt_cmd_in,
            self.mqtt_out,
            self.mqtt_last_rt,
            self.mqtt_last_time,
            self.mqtt_tracks_in_last,
            self.tracker_time,
            self.tracker_gps_lat,
            self.tracker_gps_lon,
            self.tracker_gps_alt,
            self.tracker_gps_fix,
            self.tracker_gps_numsats,
            self.tracker_gps_time,
            self.tracker_gps_tow,
            self.tracker_gps_veln,
            self.tracker_gps_vele,
            self.tracker_gps_veld,
            self.ant_last_update,
            self.azm,
            self.elv,
            self.req_azm,
            self.req_elv,
            self.ant_status,
            self.raw_azm_volts,
            self.raw_elv_volts,
            self.track_last_update,
            self.track_id,
            self.track_last_range,
            self.track_last_azm,
            self.track_last_elv,
            self.track_status,
            self.az_pending,
            self.el_pending,
            self.track_last_lat,
            self.track_last_lon,
            self.track_last_alt,
            self.current_tracks,
            self.last_cmd_time
        )

        return current_message

    except Exception as e:
        print('Could not parse object %s' % e)