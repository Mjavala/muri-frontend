from datetime import datetime
import pytz
import traceback


class filter_mqtt:
    def __init__(self):
        self.payload_0xc109 = tuple  # tuple?
        self.payload_0xd2a8 = tuple
        self.payload_stat = tuple
        self.stat_meta_keys = ["stat_time", "station", "rssi", "last_slant"]
        # need to model after DB table setup
        self.raw_meta_keys = [
            "station",
            "TIMESTAMP",
            "ADDR_FROM",
            "FRAME_TYPE",
            "FRAME",
            "gps_lat",
            "gps_lon",
            "gps_alt",
            "packet_id",
            "gps_tow",
        ]

        self.switcher = {
            "stat": self.filter_stat,
            "0xc109": self.filter_0xc109,
            "0xd2a8": self.filter_0xd2a8,
        }

    def filter_stat(self, payload, device):
        print('Got stat payload')
        # TODO: Test func
        # need rssi / slant
        if payload["station"] != "VTST1" and payload["station"] != "VGRS1":
            tempObj = []
            tree = payload
            for i, key in enumerate(self.stat_meta_keys):
                if i == 2:
                    if "receiver_1" in payload:
                        tree = payload["receiver_1"]

                elif i == 3:
                    if "tracker" in payload:
                        tree = payload["tracker"]

                v = self.tree_traverse(tree, key)
                tempObj.append(v)

            timestamp = self.timestamp_to_datetime(tempObj[0])
            tempObj[0] = timestamp
            tempObj.append(device)

            return {"topic": "stat", "message": tuple(tempObj)}
        else:
            return None

    def filter_0xc109(self, payload, device):
        print('Got 0xc109 payload')
        # print(payload['destination'])
        # need hw/cw vo1/vo2
        tempObj = []
        list_0xc109 = ["HW_Vo1", "HW_Vo2", "CW_Vo1", "CW_Vo2"]
        total_0xc109 = self.raw_meta_keys + list_0xc109
        tree = payload
        for i, key in enumerate(total_0xc109):
            if i in range(1, 5):
                if "data" in payload:
                    tree = payload["data"]
            elif i > 4:
                if payload["data"]["frame_data"] and "frame_data" in payload:
                    tree = payload["data"]["frame_data"]

            v = self.tree_traverse(tree, key)
            tempObj.append(v)

        timestamp = self.timestamp_to_datetime(tempObj[1])
        tempObj[1] = timestamp
        # alt/coords calc
        tempObj[5] = tempObj[5] / 10000000
        tempObj[6] = tempObj[6] / 10000000
        tempObj[7] = tempObj[7] / 1000

        return {"topic": "0xc109", "message": tuple(tempObj)}

    def filter_0xd2a8(self, payload, device):
        print('Got 0xd2a8 payload')
        # need hw/cw vo1/vo2
        tempObj = []
        list_0xd2a8 = ["GOND_BATT_C", "VENT_BATT_C", "Ta1_C", "Ta2_C", "Ti1_C", "Ti2_C"]
        total_0xd2a8 = self.raw_meta_keys + list_0xd2a8
        print(len(total_0xd2a8))
        tree = payload

        for i, key in enumerate(total_0xd2a8):
            if i in range(1, 5):
                if payload["data"]:
                    tree = payload["data"]
            elif i > 4:
                if payload["data"]["frame_data"]:
                    tree = payload["data"]["frame_data"]

            v = self.tree_traverse(tree, key)
            tempObj.append(v)

        timestamp = self.timestamp_to_datetime(tempObj[1])
        tempObj[1] = timestamp

        tempObj[5] = tempObj[5] / 10000000
        tempObj[6] = tempObj[6] / 10000000
        tempObj[7] = tempObj[7] / 1000

        return {"topic": "0xd2a8", "message": tuple(tempObj)}

    def tree_traverse(self, tree, key):
        for k, v in tree.items():
            if k == key:
                return v
            elif isinstance(v, dict):
                found = self.tree_traverse(v, key)
                # may need to return none in case value isn't found
                if found is not None:
                    return found
            elif k is None:
                return None

    def timestamp_to_datetime(self, ts):
        tz = pytz.timezone("America/Denver")
        dt = datetime.fromtimestamp(ts, tz).strftime("%Y-%m-%d %H:%M:%S")
        return dt

    def new(self, payload):
        if payload and payload["message"]:
            try:
                func = self.switcher.get(
                    payload["destination"], lambda x=None: "invalid message type"
                )

                result = func(payload["message"], payload["device"])
                if result:
                    return result
            except Exception as e:
                print(payload["destination"])
                print("switch ERROR: {}".format(traceback.format_exc()))
                print(payload["message"])
        else:
            return None
