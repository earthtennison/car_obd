import re
import time

def bytes_to_hex(bs):
    h = ""
    for b in bs:
        bh = hex(b)[2:]
        h += ("0" * (2 - len(bh))) + bh
    return h

def hex_to_int_ori(h):
    return int(h, 0)

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

def int_to_hexstring(n, low_to_high=True, len_string=4):
    h = str(hex(n))[2:]
    # zero padding
    h = h.zfill(len_string)
    if low_to_high:
        h = "".join(reversed([h[i:i + 2] for i in range(0, len(h), 2)]))
    return h

def hexstring_to_bytesarray(h):
    bytes_array = []
    if len(h) % 2 != 0:
        print("unvalid input!")
    for i in range(0, len(h), 2):
        bytes_array.append(bytes(h[i:i+2]))
    return bytes_array

def bytes_to_hex(bs):
    h = ""
    for b in bs:
        bh = hex(b)[2:]
        h += ("0" * (2 - len(bh))) + bh
    return h

# data = b"@@{\x00\x04213LE2019005009\x00\x00\x00\x00\x00\x10\x01\xc7Q\x81a\x05T\x81a\xc3#\x01\x00\x00\x00\x00\x00\x1e\x03\x00\x00\x00\x00\x00\x02\x04\x00\x04;O|\x15\x00\x80\x04\x01\x02\x0b\x15\x0f\x06.L\xee\xec\x02\x80\xfa\x8a\x15\x00\x00\xc0\x08OV3.2.6 2021-07-30 03\x00IDD-213LE ECEE\x00\x00\x00\x8f\xf8\r\n"
# print(type(data))
# print(bytes_to_hex(data))
# print(hex_to_int_ori("0x4EFFA200"))
# print(hex_to_int("0x4EFFA200", False))
# print(bytes("1", "utf-8"))
# print(bytes("adg", "utf-8"))
# print("asfasd".encode('ascii',errors='ignore'))
# print(hex_to_ascii("3130303131313235323939383700000000000000"))
#
# print(int_to_hexstring(0000))
# print(bytes.fromhex("ab4858"))
# print("123".zfill(5))
#
print(time.time())

# print(bytes_to_hex(b'@@)\x00\x041001112529987\x00\x00\x00\x00\x00\x00\x00\x90\x01\xff\xff\xff\xff\x00\x00;z\xa4a\xcd\xf6\r\n'))

print(time.time())

