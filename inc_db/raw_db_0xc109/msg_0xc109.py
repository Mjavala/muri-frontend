def decode(self, payload):
    try:
        self.station = payload['station']
        self.receiver = payload['receiver']
        self.timestamp = payload['data']['TIMESTAMP']
        self.addr_from = payload['data']['ADDR_FROM']
        self.rssi = payload['data']['RSSI_RX']
        self.frame_type = payload['data']['FRAME_TYPE']
        self.frame_cnt = payload['data']['FRAME_CNT']
        self.frame = payload['data']['FRAME']
        self.packet_id = payload['data']['frame_data']['packet_id']
        self.packet_num = payload['data']['frame_data']['packet_num']
        self.epoch_index = payload['data']['frame_data']['epoch index']
        self.interval_index = payload['data']['frame_data']['interval index']
        self.gps_lat = payload['data']['frame_data']['gps_lat']
        self.gps_lon = payload['data']['frame_data']['gps_lon']
        self.gps_alt = payload['data']['frame_data']['gps_alt']
        self.gps_tow = payload['data']['frame_data']['gps_tow']
        self.gps_fix = payload['data']['frame_data']['gps_fix']
        self.gps_numsats = payload['data']['frame_data']['gps_numsats']
        self.cw_sa_0 = payload['data']['frame_data']['CW_SA_0']
        self.cw_sa_1 = payload['data']['frame_data']['CW_SA_1']
        self.cw_sa_2 = payload['data']['frame_data']['CW_SA_2']
        self.cw_sa_3 = payload['data']['frame_data']['CW_SA_3']
        self.cw_sa_4 = payload['data']['frame_data']['CW_SA_4']
        self.cw_sa_5 = payload['data']['frame_data']['CW_SA_5']
        self.cw_sa_6 = payload['data']['frame_data']['CW_SA_6']
        self.cw_sa_7 = payload['data']['frame_data']['CW_SA_7']
        self.cw_sa_8 = payload['data']['frame_data']['CW_SA_8']
        self.hw_sa_0 = payload['data']['frame_data']['HW_SA_0']
        self.hw_sa_1 = payload['data']['frame_data']['HW_SA_1']
        self.hw_sa_2 = payload['data']['frame_data']['HW_SA_2']
        self.hw_sa_3 = payload['data']['frame_data']['HW_SA_3']
        self.hw_sa_4 = payload['data']['frame_data']['HW_SA_4']
        self.hw_sa_5 = payload['data']['frame_data']['HW_SA_5']
        self.hw_sa_6 = payload['data']['frame_data']['HW_SA_6']
        self.hw_sa_7 = payload['data']['frame_data']['HW_SA_7']
        self.hw_sa_8 = payload['data']['frame_data']['HW_SA_8']
        self.cw_vr1 = payload['data']['frame_data']['CW_Vr1']
        self.cw_vr2 = payload['data']['frame_data']['CW_Vr2']
        self.cw_vo1 = payload['data']['frame_data']['CW_Vo1']
        self.cw_vo2 = payload['data']['frame_data']['CW_Vo2']
        self.cw_cpot = payload['data']['frame_data']['CW_Cpot']
        self.cw_gpot = payload['data']['frame_data']['CW_Gpot']
        self.hw_vr1 = payload['data']['frame_data']['HW_Vr1']
        self.hw_vr2 = payload['data']['frame_data']['HW_Vr2']
        self.hw_vo1 = payload['data']['frame_data']['HW_Vo1']
        self.hw_vo2 = payload['data']['frame_data']['HW_Vo2']

        current_message = (
            self.station,
            self.receiver,
            self.timestamp,
            self.addr_from,
            self.rssi,
            self.frame_type,
            self.frame_cnt,
            self.frame,
            self.packet_id,
            self.packet_num,
            self.epoch_index,
            self.interval_index,
            self.gps_lat,
            self.gps_lon,
            self.gps_alt,
            self.gps_tow,
            self.gps_fix,
            self.gps_numsats,
            self.cw_sa_0,
            self.cw_sa_1,
            self.cw_sa_2,
            self.cw_sa_3,
            self.cw_sa_4,
            self.cw_sa_5,
            self.cw_sa_6,
            self.cw_sa_7,
            self.cw_sa_8,
            self.hw_sa_0,
            self.hw_sa_1,
            self.hw_sa_2,
            self.hw_sa_3,
            self.hw_sa_4,
            self.hw_sa_5,
            self.hw_sa_6,
            self.hw_sa_7,
            self.hw_sa_8,
            self.cw_vr1,
            self.cw_vr2,
            self.cw_vo1,
            self.cw_vo2,
            self.cw_cpot,
            self.cw_gpot,
            self.hw_vr1,
            self.hw_vr2,
            self.hw_vo1,
            self.hw_vo2
        )
        return current_message

    except Exception as e:
        print('Could not parse object %s' % e)