import binascii
from binascii import unhexlify
import datetime
import time

def ip_to_hex(ip):
    ip_hex = ''
    ip_split = ip.split('.') 
    p = [hex(int(i)) for i in ip_split]
    for i in p:
        ip_hex += i[2:]
    return ip_hex

def find_length(x):
    hex_length = len(x)
    byte_length = hex_length/2
    return byte_length

def get_datetime():
    time_stamp = int(time.time())
    print(datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S'))
    time_stamp_hex = hex(time_stamp)
    #Convert Hex to "Low to High", Hex per byte = 2
    time_stamp_hex_invert = "".join(reversed([time_stamp_hex[i:i + 2] for i in range(2, len(time_stamp_hex), 2)]))
    return time_stamp_hex_invert


def login_response(device_id, ip, port):
    #4040 is in Hexadecimal
    header = '4040'
    version = '04'
    device_id = bytes(device_id,'utf-8').hex()
    command_type = '9001' #command type 9001 means login response package
    #ip = '35.240.241.234'
    ip_hex = ip_to_hex(ip)
    utc_time = get_datetime()

    #TODO
    crc = ''
    tail = '0D0A'

    #TODO
    package_length = find_length(response) + 2 #add it own length

    response = header + package_length + version + device_id + command_type + ip_hex + port + utc_time + crc + tail
    response = unhexlify(response)
    return response

    


# x = '404029000431303031313132353239393837000000000000009001FFFFFFFF0000C1DE7952A5DD0D0A'
# print(len(x))
device_id = bytes('213LE2019005009','utf-8')
print(device_id.hex())
ip = '35.240.241.234'
x = ip_to_hex(ip)


print(datetime.datetime.now())
x = get_datetime()
y = unhexlify(x)
z = bytes.fromhex(x)
print(x)
print(y)
print(z)

#original package = 404029000431303031313132353239393837000000000000009001FFFFFFFF0000C1DE7952A5DD0D0A
# print(unhexlify('404029000431303031313132353239393837000000000000009001FFFFFFFF0000C1DE7952A5DD0D0A'))

#edit time and date