import socket
import select

HEADER_LENGTH = 10

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

def hex_to_int(h):
    return int(h, 0)

def receive_message(client_socket):
    try:
        # read data
        # TODO  interpret data
        message = client_socket.recv(1024)
        message = bytes_to_hex(message)
        return message

    except Exception as e:
        print(e)
        return False


while True:
    # wait until socket is ready to read
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    for notified_socket in read_sockets:
        # If notified socket is server, means new connection
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            print("new connection from {}".format(client_address))

            # received 1001 launch package
            launch_message = receive_message(client_socket)

            print(launch_message)
            # If False - obd disconnected before it sent data
            if launch_message is False:
                continue

            # register new device accepted socket
            sockets_list.append(client_socket)

            # TODO save device id to clients dict
            clients[client_socket] = "obd1"





        # else the socket send new message
        else:
            message = receive_message(notified_socket)
            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]))

                # Remove from list for socket.socket()
                sockets_list.remove(notified_socket)

                # Remove from our list of users
                del clients[notified_socket]

            device_id = clients[notified_socket]
            print("Received message from {} :\n{}".format(device_id, message))

