import socket
import select

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

a = {"name": "earth", "compatny": "motorhub"}

def receive_message(client_socket):
    try:
        # TODO  interpret data
        # protocol length 2+2+1+20+2
        header = client_socket.recv(27)
        print(bytes_to_hex(header))
        head = bytes_to_hex(header[:2])
        if head != "4040":
            return None, None
        message_length = hex_to_int(bytes_to_hex(header[2:4]))
        version = bytes_to_hex(header[4:5])
        device_id = (header[5:25]).decode().strip()
        command_type = bytes_to_hex(header[25:27])

        message = client_socket.recv(message_length - 27)
        message = bytes_to_hex(message)
        return message, device_id

    except Exception as e:
        print(e)
        return False, False

def send_heartbeat():
    

while True:
    # wait until socket is ready to read
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    for notified_socket in read_sockets:
        # If notified socket is server, means new connection
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            print("new connection from {}".format(client_address))

            # received 1001 login package
            login_message, device_id = receive_message(client_socket)

            print(login_message)
            # If False - obd disconnected before it sent data
            if login_message is False:
                continue

            # register new device accepted socket
            sockets_list.append(client_socket)

            # device_id contains 13 digits
            clients[client_socket] = device_id

            # TODO send heartbeat package
            # client_socket.send()

        # else the socket send new message
        else:
            count = 0
            while count < 2 :
                message, _ = receive_message(notified_socket)
                if message is None:
                    # try receive again
                    # print("found no header find header again")
                    pass
                else:
                    break
                count += 1

            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]))

                # Remove from list for socket.socket()
                sockets_list.remove(notified_socket)

                # Remove from our list of users
                del clients[notified_socket]

                device_id = clients[notified_socket]

            print("Received message from {} :\n{}".format(device_id, message))

