

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

def decode_date(d):
    HEX_PER_BYTE = 2
    d=str(int(d[:2],16))+'/'+str(int(d[2:4],16))+'/'+str(int(d[4:6],16))
    return d

def decode_time(t):
    HEX_PER_BYTE = 2
    t=str(int(t[:2],16))+':'+str(int(t[2:4],16))+':'+str(int(t[4:6],16))
    return t


def decode_flag(f):
    HEX_PER_BYTE = 2
    x=bin(int(f, 16))[2:].zfill(8)
    x="".join(reversed([x[i:i + 4] for i in range(0, 4, 2)]))

    z=""
    if x[:1] == '1':
        z= z+"east longitude "
    if x[:1] == '0':
        z= z+"west longitude "
    if x[1:2] == '1':
        z= z+"north lattitude "
    if x[1:2] == '0':
        z= z+"south lattitude "
    if x[2:4] == '00':
        z= z+"No fix "
    if x[2:4] == '01':
        z= z+"2D location "
    if x[2:4] == '11':
        z= z+"3D location "

    z= z + "with " + str(int(x[4:8],2)) + " satellites"

    return z


def decode_gps_data(data):
    if len(data) != 20*2:
        print(len(data))
        return False
    gps_data = {
        "date": None,
        "time": None,
        "lattitude": None,
        "longtitude": None,
        "speed": None,
        "direction": None,
        "flag": None
    }
    
    date = data[1*2:4*2]
    time = data[4*2:7*2]
    lattitude = data[7*2:11*2]
    longtitude = data[11*2:15*2]
    speed = data[15*2:17*2]
    direction = data[17*2:19*2]
    flag = data[19*2:20*2]


    gps_data["date"]=decode_date(date)
    gps_data["time"]=decode_time(time)
    gps_data["lattitude"]=hex_to_int(lattitude)/3600000
    gps_data["longtitude"]=hex_to_int(longtitude)/3600000
    gps_data["speed"]=hex_to_int(speed)
    gps_data["direction"]=hex_to_int(direction)/10
    gps_data["flag"]=decode_flag(flag)

    return gps_data


if __name__ == "__main__":
    input_data = "01190A0D04121A1480D60488C5721800000000AF"
    gps_data = decode_gps_data(input_data)
    print(gps_data)