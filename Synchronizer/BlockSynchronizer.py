from FINOChainController import Property
from CommunicationManager import Sender
from StorageManager import FileController
from socket import *
import json


def sync_block():
    import thread

    thread.start_new_thread(block_sync_receiver, ("BlockReceiver", 1))
    request_block_sync()


def request_block_sync():

    trust_node_ip = Property.trust_node_ip
    last_file = FileController.get_last_file()

    req_json_obj = {
        'type': 'RB',
        'last_file': last_file,
        'ip_address': Property.my_ip_address
    }

    req_json_str = json.dumps(req_json_obj)
    Sender.send(trust_node_ip, req_json_str, Property.port)


def block_sync_receiver(*args):
    addr = (Property.my_ip_address, Property.port)
    buf_size = 10000

    tcp_socket = socket(AF_INET, SOCK_STREAM)
    tcp_socket.bind(addr)
    tcp_socket.listen(5)

    while True:

        receive_socket, sender_ip = tcp_socket.accept()

        while True:
            data = receive_socket.recv(buf_size)
            try:
                if data == "":
                    break

                data_json_obj = json.loads(data)

                if data_json_obj['type'] == 'CBSYNC':
                    Property.block_sync = True
                    break

                elif data_json_obj['type'] == "BSYNC":
                    FileController.write(FileController.block_storage_path + data_json_obj['file_name'], data_json_obj['message'])

            except:
                break

        if Property.block_sync is True:
            receive_socket.close()
            tcp_socket.close()
            break


