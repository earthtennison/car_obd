from binascii import unhexlify
from crc_util import CRC
import time


def encode_ip(ip):
    """
    convert ip address to hexstring
    example input: 211.139.196.166
    example output: D38BC4A6
    """
    ip_hex = ''
    ip_split = ip.split('.')
    p = [hex(int(i)) for i in ip_split]
    for i in p:
        ip_hex += i[2:]
    return ip_hex


def encode_port(n, low_to_high=True, len_string=4):
    h = str(hex(n))[2:]
    # zero padding
    h = h.zfill(len_string)
    if low_to_high:
        h = "".join(reversed([h[i:i + 2] for i in range(0, len(h), 2)]))
    return h


def encode_datetime():
    time_stamp = int(time.time())
    # print(datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S'))
    time_stamp_hex = hex(time_stamp)
    # Convert Hex to "Low to High", Hex per byte = 2
    time_stamp_hex_invert = "".join(reversed([time_stamp_hex[i:i + 2] for i in range(2, len(time_stamp_hex), 2)]))
    return time_stamp_hex_invert


# def find_length(x):
#     hex_length = len(x)
#     byte_length = hex_length / 2
#     return byte_length

def login_response(device_id, ip='35.240.241.234', port=1234):
    # 4040 is in Hexadecimal
    header = '4040'
    package_length = "2900"
    version = '04'
    device_id = bytes(device_id, 'utf-8').hex().ljust(40, '0')
    command_type = '9001'  # command type 9001 means login response package
    ip_hex = encode_ip(ip)  # ip = '35.240.241.234'
    port_hex = encode_port(port, low_to_high=True, len_string=4)
    utc_time = encode_datetime()  # "C1DE7952" is used in example

    crc_util = CRC()
    # hexstring to bytesarray
    data_for_crc = header + package_length + version + device_id + command_type + ip_hex + port_hex + utc_time
    data_for_crc = data_for_crc.upper()
    data_for_crc = unhexlify(data_for_crc)
    crc = crc_util.make_crc(data_for_crc, len(data_for_crc))
    # low to high
    crc = "".join(reversed([crc[i:i + 2] for i in range(0, len(crc), 2)]))
    tail = '0D0A'

    response = header + package_length + version + device_id + command_type + ip_hex + port_hex + utc_time + crc + tail
    response = unhexlify(response)
    return response


if __name__ == "__main__":
    print(login_response("213LE2019005009", ip="255.255.255.255", port=0000))
