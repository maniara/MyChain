from socket import *

import node


def send(ip_address, message, port, *args):
    receiver_addr = (ip_address, port)
    tcp_socket = socket(AF_INET, SOCK_STREAM)

    try:
        tcp_socket.connect(receiver_addr)
        tcp_socket.sendall(message.encode('utf-8'))

    except Exception as e:
        print("Connection Failed while sending", e)

def send_to_all_node(message):
    address_list = list(map(lambda x: x.ip_address, node.get_all()))

    for addr in address_list:
        try:
            send(addr, message, 3000, 1)
        except Exception as e:
            print("SENDTOALL EXCEPT", e)
