from socket import *

from FINOChainController import Property
from StorageManager import FileController


def send(ip_address, message, port):
    receiver_addr = (ip_address, port)
    tcp_socket = socket(AF_INET, SOCK_STREAM)

    try:
        tcp_socket.connect(receiver_addr)
        tcp_socket.sendall(message.encode())

    except Exception as e:
        print("Connection Failed while sending", e)



def send_to_all_node(message):

    address_list = FileController.get_ip_list()

    for addr in address_list:
        if addr != Property.my_ip_address:
            try:
                send(addr, message, Property.port)
            except Exception as e:
                print("SENDTOALL EXCEPT")
        else:
            continue
