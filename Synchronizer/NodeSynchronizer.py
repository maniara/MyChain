from FINOChainController import Property
from NodeManager import NodeController
from CommunicationManager import Sender
import json
from socket import *


def download_node_list(my_node):
    import thread
    thread.start_new_thread(node_sync_receiver, ("NodeReceiver", 1))
    request_node_list()


def request_node_list():

    trust_node_ip = Property.trust_node_ip
    req_json_obj = {
        'type': 'RN',
        'ip_address': Property.my_ip_address
    }
    req_json_str = json.dumps(req_json_obj)
    Sender.send(trust_node_ip, req_json_str, Property.port)


def node_sync_receiver(*args):

    print "Enter Node_Sync"
    addr = (Property.my_ip_address, Property.port)
    buf_size = 10000

    tcp_socket = socket(AF_INET, SOCK_STREAM)
    tcp_socket.bind(addr)
    tcp_socket.listen(5)

    while True:
        print "WAIT"
        receive_socket, sender_ip = tcp_socket.accept()

        while True:
            data = receive_socket.recv(buf_size)
            try:
                if data == "":
                    break

                node_json_obj = json.loads(data)
                print "Receiving" + node_json_obj['type']

                if node_json_obj['type'] == 'CNSYNC':
                    print "CNSYNC"
                    Property.node_sync = True
                    break

                elif node_json_obj['type'] == 'N':
                    NodeController.add_new_node(json.loads(node_json_obj['message']))

            except:
                break

        if Property.node_sync is True:
            tcp_socket.close()
            receive_socket.close()
            print "Thread Closed"
            break