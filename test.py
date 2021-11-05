import socket
#hahahahahhaha
def bytes_to_hex(bs):
    h = ""
    for b in bs:
        bh = hex(b)[2:]
        h += ("0" * (2 - len(bh))) + bh
    return h

def hex_to_int(h):
    return int(h, 0)

data = b"@@{\x00\x04213LE2019005009\x00\x00\x00\x00\x00\x10\x01\xc7Q\x81a\x05T\x81a\xc3#\x01\x00\x00\x00\x00\x00\x1e\x03\x00\x00\x00\x00\x00\x02\x04\x00\x04;O|\x15\x00\x80\x04\x01\x02\x0b\x15\x0f\x06.L\xee\xec\x02\x80\xfa\x8a\x15\x00\x00\xc0\x08OV3.2.6 2021-07-30 03\x00IDD-213LE ECEE\x00\x00\x00\x8f\xf8\r\n"
print(type(data))
print(bytes_to_hex(data))
print(hex_to_int("0x000123c3"))
print(bytes("1", "utf-8"))
print(bytes("adg", "utf-8"))
print("asfasd".encode('ascii',errors='ignore'))


