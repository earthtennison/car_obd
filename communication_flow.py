import socket
import select
import config
from login_response import login_response
from heartbeat_response import heartbeat_response
from obd_stat_data_decoder import decode_stat_data
from obd_gps_decoder import decode_gps_data
from obd_pid_decoder import decode_pid_data, decode_pid_type
from database_management import Cosmos_DB


HOST = config.settings['host']
MASTER_KEY = config.settings['master_key']
DATABASE_ID = config.settings['database_id']
CONTAINER_ID = config.settings['container_id']
IP = "0.0.0.0"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))

server_socket.listen()

sockets_list = [server_socket]
clients = {}

print("Listening for connections on {}:{}...".format(IP, PORT))


def bytes_to_hex(bs):
    h = ""
    for b in bs:
        bh = hex(b)[2:]
        h += ("0" * (2 - len(bh))) + bh
    return h


def hex_to_int(h, is_low_to_high=True):
    if len(h) > 2 and h[:2] == "0x":
        if is_low_to_high:
            h = h[:2] + "".join(reversed([h[i:i + 2] for i in range(2, len(h), 2)]))
        return int(h, 0)
    else:
        if is_low_to_high:
            h = "".join(reversed([h[i:i + 2] for i in range(0, len(h), 2)]))
        return int(h, 16)


def hex_to_ascii(h):
    bytes_object = bytes.fromhex(h)
    return bytes_object.decode("ASCII")


def receive_message(client_socket):
    try:
        # protocol length 2+2+1+20+2
        header = client_socket.recv(27)
        header_hex = bytes_to_hex(header)
        # print(bytes_to_hex(header))
        head = bytes_to_hex(header[:2])
        if head != "4040":
            return None, None, None
        message_length = hex_to_int(bytes_to_hex(header[2:4]))
        version = bytes_to_hex(header[4:5])
        device_id = (header[5:25]).decode().strip()
        command_type = bytes_to_hex(header[25:27])

        message = client_socket.recv(message_length - 27)
        message = bytes_to_hex(message)

        # TODO check crc

        return header_hex, message, (message_length, version, device_id, command_type)

    except Exception as e:
        print(e)
        return False, False, False


def interpret_login_message(payload):
    data = {}
    stat_data = decode_stat_data(payload[0:34 * 2])
    gps_data = decode_gps_data(payload[34 * 2:54 * 2])
    data["stat_data"] = stat_data
    data["gps_data"] = gps_data
    return data


def interpret(payload, command_type):
    """interpret payload in hexstring"""
    data = {}
    if command_type == "4002":
        stat_data = decode_stat_data(payload[0:34 * 2])
        sample_rate = hex_to_int(payload[34 * 2:36 * 2])
        pid_type_count = hex_to_int(payload[36 * 2:37 * 2])
        pid_type_array = decode_pid_type(payload[37 * 2:(37 + pid_type_count * 2) * 2])
        n = (37 + pid_type_count * 2)
        pid_group_count = hex_to_int(payload[n * 2: (n + 1) * 2])
        pid_group_size = hex_to_int(payload[(n + 1) * 2: (n + 2) * 2])
        m = n + 2
        # pid_data = decode_pid_data(payload[m * 2: (m + pid_group_count * pid_group_size) * 2], pid_type_array)

        data["stat_data"] = stat_data
        # data["pid_data"] = pid_data

    elif command_type == "4001":

        stat_data = decode_stat_data(payload[1 * 2:35 * 2])
        # TODO interpret gps data

        data["stat_data"] = stat_data

    return data


if __name__ == "__main__":
    cosmos = Cosmos_DB(HOST,MASTER_KEY,DATABASE_ID,CONTAINER_ID)
    while True:
        # wait until socket is ready to read
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
        for notified_socket in read_sockets:
            # If notified socket is server, means new connection
            if notified_socket == server_socket:
                client_socket, client_address = server_socket.accept()
                print("new connection from {}".format(client_address))

                # received 1001 login package
                header_message, login_message, metadata = receive_message(client_socket)
                device_id = metadata[2]
                print('Device ID is {}'.format(device_id))
                print("header message", header_message)
                print("login message", login_message)
                # If False - obd disconnected before it sent data
                if login_message is False:
                    continue

                # register new device accepted socket
                sockets_list.append(client_socket)

                # device_id contains 13 digits
                clients[client_socket] = device_id

                # interpret data
                interpret_data = interpret_login_message(login_message)
                # TODO push to cloud
                if interpret_data:
                    print("[{}] push to cloud: {}".format(metadata[3], interpret_data))
                    interpret_data['package'] = metadata[3]
                    cosmos.upsert_item(interpret_data)

                # send heartbeat login package 9001
                # use Sinocastel's recommendation default ip and port
                login_res = login_response(device_id, ip="255.255.255.255", port=0000)
                print("Login response: ", login_res)
                client_socket.send(login_res)

                print('- ' * 40)

            # else the socket send new message
            else:
                count = 0
                message = None
                while count < 2:
                    header_message, message, metadata = receive_message(notified_socket)
                    if message is not None:
                        break
                    else:
                        # try receive again
                        # print("found no header find header again")
                        count += 1
                        continue

                if message is not None:
                    device_id = clients[notified_socket]
                    # print("Received message from {} :\nheader:{}\npayload:{}".format(metadata[2], header_message,
                    #                                                                  message))
                    print('- ' * 40)

                    # TODO  interpret data
                    interpret_data = interpret(message, metadata[3])
                    interpret_data["package"] = metadata[3]
                    if interpret_data:
                        print("[{}] push to cloud: {}".format(metadata[3], interpret_data))
                        cosmos.upsert_item(interpret_data)

                    # check if it heartbeat package 1003 (send every 2 minutes)
                    # send heartbeat response package 9003
                    if metadata[3] == "1003":
                        heartbeat_res = heartbeat_response(metadata[2])
                        notified_socket.send(heartbeat_res)

                    # TODO push data to cloud


                elif message is False:
                    print('Closed connection from: {}'.format(clients[notified_socket]))

                    # Remove from list for socket.socket()
                    sockets_list.remove(notified_socket)

                    # Remove from our list of users
                    del clients[notified_socket]
