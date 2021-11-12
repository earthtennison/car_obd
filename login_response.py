import binascii
from binascii import unhexlify
import datetime
    
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
    time_stamp = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
    time_stamp_hex = hex(int(time_stamp))
    return time_stamp_hex[2:]

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
print(x)
print(unhexlify(x))
print(unhexlify(device_id.hex()))
print(unhexlify(x+device_id.hex()))

time_stamp = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
time_stamp_hex = hex(int(time_stamp))
print(time_stamp_hex)
#print(unhexlify(get_datetime()))
#original package = 404029000431303031313132353239393837000000000000009001FFFFFFFF0000C1DE7952A5DD0D0A
