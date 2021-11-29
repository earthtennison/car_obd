import time
from datetime import datetime
def bytes_to_hex(bs):
    h = ""
    for b in bs:
        bh = hex(b)[2:]
        h += ("0" * (2 - len(bh))) + bh
    return h

def hex_to_int(h, is_low_to_high=True):
    HEX_PER_BYTE = 2
    if len(h)>2 and h[:2] == "0x":
        if is_low_to_high == True:
            h = h[:2] + "".join(reversed([h[i:i + 2] for i in range(2, len(h), 2)]))
        return int(h, 0)
    else:
        if is_low_to_high == True:
            h = "".join(reversed([h[i:i + 2] for i in range(0, len(h), 2)]))
        return int(h, 16)

def hex_to_ascii(h):
    bytes_object = bytes.fromhex(h)
    return bytes_object.decode("ASCII")

def decode_data_time(d):
    """translate unix time in second to readable format"""
    d = hex_to_int(d, True)
    d = datetime.utcfromtimestamp(d).strftime('%Y-%m-%d %H:%M:%S')
    return d

def decode_vstate(v):
    # TODO
    return v

def decode_reserved(r):
    # TODO
    return r

def decode_stat_data(data):
    if len(data) != 34*2:
        print(len(data))
        return False
    stat_data = {
        "last_accon_time": None,
        "UTC_Time": None,
        "total_trip_mileage": None,
        "current_trip_mileage": None,
        "total_fuel": None,
        "current_fuel": None,
        "vstate": None,
        "reserved": None
    }

    last_accon_time = data[:4*2]
    UTC_Time = data[4*2:8*2]
    total_trip_mileage = data[8*2:12*2]
    current_trip_mileage = data[12*2:16*2]
    total_fuel = data[16*2:20*2]
    current_fuel = data[20*2:22*2]
    vstate = data[22*2:26*2]
    reserved = data[26*2:]

    stat_data["last_accon_time"] = decode_data_time(last_accon_time)
    stat_data["UTC_Time"] = decode_data_time(UTC_Time)
    stat_data["total_trip_mileage"] = hex_to_int(total_trip_mileage)
    stat_data["current_trip_mileage"] = hex_to_int(current_trip_mileage)
    stat_data["total_fuel"] = hex_to_int(total_fuel) # in 0.01 L
    stat_data["current_fuel"] = hex_to_int(current_fuel)
    stat_data["vstate"] = decode_vstate(vstate)
    stat_data["reserved"] = decode_reserved(reserved)

    return stat_data

def get_stat_data():
    input_data = "C1F06952FDF069529C91110000000000698300000C0000000000036401014C000300"
    stat_data = decode_stat_data(input_data)
    return stat_data

if __name__ == "__main__":
    input_data = "146ba461ff6fa461c32301000000000021030000000000020400003b4f7c15000004"
    stat_data = decode_stat_data(input_data)
    print(stat_data)

