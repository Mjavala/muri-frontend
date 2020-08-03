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
        self.gps_lat = payload['data']['frame_data']['gps_lat']
        self.gps_lon = payload['data']['frame_data']['gps_lon']
        self.gps_alt = payload['data']['frame_data']['gps_alt']
        self.gps_tow = payload['data']['frame_data']['gps_tow']
        self.gps_fix = payload['data']['frame_data']['gps_fix']
        self.gps_numsats = payload['data']['frame_data']['gps_numsats']
        self.gond_batt = payload['data']['frame_data']['GOND_BATT']
        self.gond_sta =  payload['data']['frame_data']['GOND_STA']
        self.rs41_temp =  payload['data']['frame_data']['RS41_Temp']
        self.rs41_hum = payload['data']['frame_data']['RS41_Hum']
        self.rs41_pres = payload['data']['frame_data']['RS41_Pres']
        self.rs41_stat = payload['data']['frame_data']['RS41_Stat']
        self.ta1 = payload['data']['frame_data']['Ta1']
        self.ti1 = payload['data']['frame_data']['Ti1']
        self.ta2 = payload['data']['frame_data']['Ta2']
        self.ti2 = payload['data']['frame_data']['Ti2']
        self.cw_cp_vr1 = payload['data']['frame_data']['CW_CP_Vr1']
        self.cw_cp_vr2 = payload['data']['frame_data']['CW_CP_Vr2']
        self.cw_cp_vo1 = payload['data']['frame_data']['CW_CP_Vo1']
        self.cw_cp_vo2 = payload['data']['frame_data']['CW_CP_Vo2']
        self.cw_cp_cpot = payload['data']['frame_data']['CW_CP_Cpot']
        self.cw_cp_gpot = payload['data']['frame_data']['CW_CP_Gpot']
        self.gps_veln = payload['data']['frame_data']['gps_veln']
        self.gps_vele = payload['data']['frame_data']['gps_vele']
        self.gps_veld = payload['data']['frame_data']['gps_veld']
        self.hw_cp_vr1 = payload['data']['frame_data']['HW_CP_Vr1']
        self.hw_cp_vr2 = payload['data']['frame_data']['HW_CP_Vr2']
        self.hw_cp_vo1 = payload['data']['frame_data']['HW_CP_Vo1']
        self.hw_cp_vo2 = payload['data']['frame_data']['HW_CP_Vo2']
        self.hw_cp_cpot = payload['data']['frame_data']['HW_CP_Cpot']
        self.hw_cp_gpot = payload['data']['frame_data']['HW_CP_Gpot']
        self.gps_rms_hor = payload['data']['frame_data']['gps_rms_hor']
        self.gps_rms_ver = payload['data']['frame_data']['gps_rms_ver']
        self.vent_batt = payload['data']['frame_data']['VENT_BATT']
        self.vent_stat = payload['data']['frame_data']['VENT_STAT']
        self.vent_ta1 = payload['data']['frame_data']['VENT_Ta1']
        self.vent_ti1 = payload['data']['frame_data']['VENT_Ti1']
        self.vent_ta2 = payload['data']['frame_data']['VENT_Ta2']
        self.vent_ti2 = payload['data']['frame_data']['VENT_Ti2']
        self.vent_diff = payload['data']['frame_data']['VENT_DIFF']
        self.gond_batt_c = payload['data']['frame_data']['GOND_BATT_C']
        self.vent_batt_c = payload['data']['frame_data']['VENT_BATT_C']
        self.ta1_c = payload['data']['frame_data']['Ta1_C']
        self.ti1_c = payload['data']['frame_data']['Ti1_C']
        self.ta2_c = payload['data']['frame_data']['Ta2_C']
        self.ti2_c = payload['data']['frame_data']['Ti2_C']
        self.vent_ta1_c = payload['data']['frame_data']['VENT_Ta1_C']
        self.vent_ti1_c = payload['data']['frame_data']['VENT_Ti1_C']
        self.vent_ta2_c = payload['data']['frame_data']['VENT_Ta2_C']
        self.vent_ti2_c = payload['data']['frame_data']['VENT_Ti2_C']
        self.gps_veln_c = payload['data']['frame_data']['gps_veln_C']
        self.gps_vele_c = payload['data']['frame_data']['gps_vele_C']
        self.gps_veld_c = payload['data']['frame_data']['gps_veld_C']
        self.converted = payload['data']['converted']

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
            self.gps_lat,
            self.gps_lon,
            self.gps_alt,
            self.gps_tow,
            self.gps_fix,
            self.gps_numsats,
            self.gond_batt,
            self.gond_sta,
            self.rs41_temp,
            self.rs41_hum,
            self.rs41_pres,
            self.rs41_stat,
            self.ta1,
            self.ti1,
            self.ta2,
            self.ti2,
            self.cw_cp_vr1,
            self.cw_cp_vr2,
            self.cw_cp_vo1,
            self.cw_cp_vo2,
            self.cw_cp_cpot,
            self.cw_cp_gpot,
            self.gps_veln,
            self.gps_vele,
            self.gps_veld,
            self.hw_cp_vr1,
            self.hw_cp_vr2,
            self.hw_cp_vo1,
            self.hw_cp_vo2,
            self.hw_cp_cpot,
            self.hw_cp_gpot,
            self.gps_rms_hor,
            self.gps_rms_ver,
            self.vent_batt,
            self.vent_stat,
            self.vent_ta1,
            self.vent_ti1,
            self.vent_ta2,
            self.vent_ti2,
            self.vent_diff,
            self.gond_batt_c,
            self.vent_batt_c,
            self.ta1_c,
            self.ti1_c,
            self.ta2_c,
            self.ti2_c,
            self.vent_ta1_c,
            self.vent_ti1_c,
            self.vent_ta2_c,
            self.vent_ti2_c,
            self.gps_veln_c,
            self.gps_vele_c,
            self.gps_veld_c,
            self.converted
        )
        return current_message

    except Exception as e:
        print('Could not parse object %s' % e)