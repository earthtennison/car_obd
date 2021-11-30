from crc_util import CRC
from binascii import unhexlify


def heartbeat_response(device_id):
    header = '4040'
    package_length = "1F00"
    version = '04'
    device_id = bytes(device_id, 'utf-8').hex().ljust(40, '0')
    command_type = '9003'  # command type 9001 means login response package
    crc_util = CRC()
    # hexstring to bytesarray
    data_for_crc = header + package_length + version + device_id + command_type
    data_for_crc = data_for_crc.upper()
    data_for_crc = unhexlify(data_for_crc)
    # make crc
    crc = crc_util.make_crc(data_for_crc, len(data_for_crc))
    # low to high
    crc = "".join(reversed([crc[i:i + 2] for i in range(0, len(crc), 2)]))
    tail = '0D0A'

    response = header + package_length + version + device_id + command_type + crc + tail
    response = unhexlify(response)
    return response

if __name__ == "__main__":
    print(heartbeat_response("213LE2019005009"))