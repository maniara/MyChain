import traceback
from socket import *
from venv import logger

import key
import node
import transaction
from block import create_block
from key import __init__
from transaction import remove_all, Transaction


def start(thread_name, ip_address, port):
    import json

    addr = (ip_address, port)
    buf_size = 1024

    tcp_socket = socket(AF_INET, SOCK_STREAM)
    tcp_socket.bind(addr)
    tcp_socket.listen(5)

    while True:

        receive_socket, sender_ip = tcp_socket.accept()

        while True:
            print("Receiving")
            data = receive_socket.recv(buf_size)
            try:

                if len(data) == 0:
                    break

                data_json_obj = json.loads(data)

                if data_json_obj['type'] == 'T':
                    logger.info("Receiving a transaction")

                    verify_msg = data_json_obj['time_stamp'] + data_json_obj['message']

                    verification = key.verify_signature(data_json_obj['pub_key'], data_json_obj['signature'],
                                                             verify_msg)

                    if verification is True:
                        print("Transaction is valid")
                        tx = Transaction().from_json(data_json_obj)
                        transaction.add_transaction(tx)

                elif data_json_obj['type'] == 'N':
                    from node import node_controller

                    node_list = node.get_all()
                    received_ip = data_json_obj['ip_address']
                    sync_flag = False

                    for outer_list in node_list:
                        outer_list = str(outer_list)
                        if outer_list == received_ip:
                            sync_flag = True

                    if sync_flag is False:
                        node_controller.add_new_node(data_json_obj)

                # When received block, add to file database
                elif data_json_obj['type'] == 'B':
                    transaction.remove_all()
                    create_block(data_json_obj['block_id'], data)

            except:
                traceback.print_exc()
                break

    tcp_socket.close()
    receive_socket.close()
