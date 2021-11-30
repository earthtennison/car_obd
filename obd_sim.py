import socket
import time
import errno
import sys
from binascii import unhexlify

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)


def bytes_to_hex(bs):
    h = ""
    for b in bs:
        bh = hex(b)[2:]
        h += ("0" * (2 - len(bh))) + bh
    return h


'''
example data
1. launch package:
b"@@{\x00\x04213LE2019005009\x00\x00\x00\x00\x00\x10\x01\xc7Q\x81a\x05T\x81a\xc3#\x01\x00\x00\x00\x00\x00\x1e\x03\x00\x00\x00\x00\x00\x02\x04\x00\x04;O|\x15\x00\x80\x04\x01\x02\x0b\x15\x0f\x06.L\xee\xec\x02\x80\xfa\x8a\x15\x00\x00\xc0\x08OV3.2.6 2021-07-30 03\x00IDD-213LE ECEE\x00\x00\x00\x8f\xf8\r\n"
'''

if __name__ == "__main__":
    data = "@@{\x00\x04213LE2019005009\x00\x00\x00\x00\x00\x10\x01\xc7Q\x81a\x05T\x81a\xc3#\x01\x00\x00\x00\x00\x00\x1e" \
           "\x03\x00\x00\x00\x00\x00\x02\x04\x00\x04;O|\x15\x00\x80\x04\x01\x02\x0b\x15\x0f\x06.L\xee\xec\x02\x80\xfa" \
           "\x8a\x15\x00\x00\xc0\x08OV3.2.6 2021-07-30 03\x00IDD-213LE ECEE\x00\x00\x00\x8f\xf8\r\n "

    # login state
    while True:
        client_socket.send(bytes(data, "utf-8"))
        print("Send {}...".format(data[:20]))
        time.sleep(1)

        try:
            heartbeat = client_socket.recv(41)
            # if error not throw it receive login succesfully
            heartbeat_hex = bytes_to_hex(heartbeat)
            print("Heartbeat login response: ", heartbeat_hex)
            command_type = bytes_to_hex(heartbeat[25:27])
            if command_type == "9001":
                break
        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error: {}'.format(str(e)))
                sys.exit()

            # We just did not receive anything
            time.sleep(1)
            continue

    # catch keyboard interupt to properly close the socket
    try:
        # data flow state
        beat_start = time.time()
        while True:
            # package 4004 support PIDs
            support_pid = "404086000431303031313132353239393837000000000000004004C1F0695200F169529C91110000000000698300000" \
                          "D0000000400036401014C00030022032104210521062107210C210D210E210F2110211121132115211C211F2121212" \
                          "4212E212F2130213121322133213C214221432144214521472149214A214C214D214E219AE90D0A"

            # package 4006 DTC
            dtc = "404043000431303031313132353239393837000000000000004006C1F0695209F169529C91110000000000698300000D00000004" \
                  "00036401014C00030000009AF40D0A"
            # package 4005 freeze frame
            freeze_frame = ""
            # package 4001 GPS
            gps = "40405900043130303131313235323939383700000000000000400101C1F06952E7F069529C911100000000006983000" \
                  "0070000000400036401014C00030001190A0D0412041480D60488C57218000000009F01E803ED9A0D0A"
            # package 4002 OBD data
            obd = "404057000431303031313132353239393837000000000000004002C1F06952F0F169529C91110000000000698300004" \
                  "70000000400036401014C01030078000505210C210D210F21102101073BE8030064280AEB930D0A"
            # package 4003 G-sensor
            g_sensor = ""

            data_flow = [support_pid, dtc, freeze_frame, gps, obd, g_sensor]
            for data in data_flow:
                client_socket.send(unhexlify(data))
                time.sleep(0.5)

            time.sleep(2)

            # package 1003 heartbeat every 2 minutes (for simulation use 10 second instead
            if round(time.time() - beat_start) > 10:
                while True:
                    heartbeat = "40401F00043130303131313235323939383700000000000000100303320D0A"
                    client_socket.send(unhexlify(heartbeat))
                    time.sleep(1)
                    try:
                        heartbeat = client_socket.recv(31)
                        # if error not throw it receive login succesfully
                        heartbeat_hex = bytes_to_hex(heartbeat)
                        print("Heartbeat response: ", heartbeat_hex)
                        command_type = bytes_to_hex(heartbeat[25:27])
                        if command_type == "9003":
                            break
                    except IOError as e:
                        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                            print('Reading error: {}'.format(str(e)))
                            sys.exit()

                        # We just did not receive anything
                        time.sleep(1)
                        continue
    except KeyboardInterrupt:
        print("Keyboard Interrupted")
        client_socket.shutdown(socket.SHUT_RDWR)
        client_socket.close()
        sys.exit(0)
