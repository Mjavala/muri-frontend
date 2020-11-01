import pytest
from historical_flights import filter_messages

# - Payload fail states
## No payload body
## payload topic not found
## No payload
## VGRS/VST1 Test

filters = filter_messages.filter_mqtt()

empty_payload = {}

# expected return ~ parsing error
empty_message = {
    'destination': 'stat',
    'message': {

    }
}
# expected return ~ lambda: "invalid message type"
bad_destination = {
    'destination': 'WOLOLOLOLO',
    'message': {
        'station': 'BARN1'
    }
}
# expected return ~ None
virtual_station = {
    'destination': 'stat',
    'message': {
        'station': 'VGRS1'
    }
}
# ["stat_time", "station", "rssi", "last_slant"]
# expected outcome ~ (100, 'BARN1', 97, 102)
good_stat =  {
    'destination': 'stat',
    'message': {
        'stat_time': 1600729946, # 2020-09-21 17:12:26,
        'sladoop': True,
        'station': 'BARN1',
        'ex': 32432,
        'reciever_1': {
            'rssi': 97,
        },
        'rand': 3,
        'tracker': {
            'last_slant': 102
        }
    }
}
# expected return ~ ('BARN1', '2020-09-21 17:12:26', 'device_id', '0xc109', '2qeqws', 1.0, 1.0, 1.0, 1234, 20, 2030, 20, 666, 32)
good_0xc = {
    'destination': '0xc109',
    'message': {
        "data": {
            "station": 'BARN1',
            "TIMESTAMP": 1600729946, # 2020-09-21 17:12:26
            "ADDR_FROM": 'device_id',
            "FRAME_TYPE": '0xc109',
            "FRAME": '2qeqws',
            "frame_data": {
                "gps_lat": 10000000, # / 10000000
                "gps_lon": 10000000, # / 10000000
                "gps_alt": 1000, # / 1000
                "packet_id": 1234,
                "gps_tow": 20,
                # add hw/cw
                "HW_Vo1": 2030,
                "HW_Vo2": 20,
                "CW_Vo1": 666,
                "CW_Vo2": 32
            }
        },
    }
}
# expected return ~ ('BARN1', '2020-09-21 16:12:26', 'device_id', '0xc109', '2qeqws', 1, 1, 1, 20, 1234, 232, 322, 40, 32.1, 20, 12.321)
good_0xd = {
    'destination': '0xd2a8',
    'message': {
        'data': {
            "station": 'BARN1',
            "TIMESTAMP": 1600729946, # 2020-09-21 17:12:26
            "ADDR_FROM": 'device_id',
            "FRAME_TYPE": '0xd2a8',
            "FRAME": '2qeqws',
            "frame_data": {
                "gps_lat": 10000000,   # / 10000000
                "gps_lon": 10000000,  # / 10000000
                "gps_alt": 1000,  # / 1000
                "packet_id": 1234,
                "gps_tow": 20,
                "GOND_BATT_C": 232,
                "VENT_BATT_C": 322,
                "Ta1_C": 40,
                "Ta2_C": 32.1, 
                "Ti1_C": 20, 
                "Ti2_C": 12.321
            }
        }
    }
}

# empty payload test
def test_empty_payload():
    assert filters.new(empty_payload) == None

def test_empty_message():
    assert filters.new(empty_message) == None

def test_bad_destination():
    assert filters.new(bad_destination) == "invalid message type"

def test_virtual_station():
    assert filters.new(virtual_station) == None

def test_good_stat():
    assert filters.new(good_stat) == {
        'topic': 'stat',
        'message': ('2020-09-21 17:12:26', 'BARN1', 97, 102)
        }

def test_good_0xc():
    assert filters.new(good_0xc) == {
        'topic': '0xc109',
        'message': ('BARN1', '2020-09-21 17:12:26', 'device_id', '0xc109', '2qeqws', 1.0, 1.0, 1.0, 1234, 20, 2030, 20, 666, 32)
    }

def test_good_0cd():
    assert filters.new(good_0xd) == {
        'topic': '0xd2a8',
        'message': ('BARN1', '2020-09-21 17:12:26', 'device_id', '0xd2a8', '2qeqws', 1.0, 1.0, 1.0, 1234, 20, 232, 322, 40, 32.1, 20, 12.321)
    }