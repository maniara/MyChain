import threading
import traceback
from socket import *

from BlockManager import BlockGenerator
from CommunicationManager import Sender
from ConsensusManager import VoteController
from FINOChainController import Property
from NodeManager import KeyController
from StorageManager import FileController


def start(thread_name, ip_address, port):
    import json

    addr = (ip_address, port)
    buf_size = 10000

    tcp_socket = socket(AF_INET, SOCK_STREAM)
    tcp_socket.bind(addr)
    tcp_socket.listen(5)

    while True:
        # Property.ui_frame.write_log("Receiver Started")
        receive_socket, sender_ip = tcp_socket.accept()

        while True:
            data = receive_socket.recv(buf_size)
            try:
                if data == "":
                    break

                data_json_obj = json.loads(data)

                if data_json_obj['type'] == 'T':

                    verify_msg = data_json_obj['time_stamp'] + data_json_obj['message']

                    verification = KeyController.verify_signature(data_json_obj['pub_key'], data_json_obj['signature'],
                                                                  verify_msg)

                    if verification is True:
                        FileController.add_transaction(data)


                elif data_json_obj['type'] == 'N':
                    from NodeManager import NodeController

                    node_list = FileController.get_ip_list()
                    received_ip = data_json_obj['ip_address']
                    sync_flag = False

                    for outer_list in node_list:
                        outer_list = str(outer_list)
                        if outer_list == received_ip:
                            sync_flag = True

                    if sync_flag is False:
                        NodeController.add_new_node(data_json_obj)

                # When received block, add to file database
                elif data_json_obj['type'] == 'B':
                    FileController.remove_all_transactions()
                    FileController.remove_all_vote()
                    FileController.create_new_block(data_json_obj['block_id'], data)




                # When received vote, calculate vote result
                # then, Check Block generation signal & delegated node.
                elif data_json_obj['type'] == 'V':

                    FileController.add_vote(str(data))

                    # When voting is finished
                    if VoteController.block_gen_signal() is True:

                        vote_result = VoteController.get_vote_result(data_json_obj['delegated_num'])

                        # Check block gen node and majority of voting
                        if data_json_obj['delegated_num'] == Property.peer_number \
                                and vote_result == data_json_obj['delegated_num']:
                            FileController.remove_all_vote()

                            t = threading.Thread(target=BlockGenerator.generate_block, args=())
                            t.start()

                # When received node sync, Send my node list to request node
                elif data_json_obj['type'] == 'RN':
                    node_list = FileController.get_node_list()

                    for node in node_list:
                        node_json_obj = {
                            'type': 'N',
                            'message': node
                        }
                        node_json_str = json.dumps(node_json_obj)
                        Sender.send(data_json_obj['ip_address'], node_json_str, port)

                    complete_json_obj={
                        'type': 'CNSYNC'
                    }
                    complete_json_str = json.dumps(complete_json_obj)
                    Sender.send(data_json_obj['ip_address'], complete_json_str, port)
                    break

                # When received [block sync], Send blocks to the request node
                elif data_json_obj['type'] == 'RB':
                    last_file = FileController.get_last_file()

                    # Not need to sync
                    if last_file == data_json_obj['last_file']:

                        bsync_json_obj = {
                            'type': 'CBSYNC'
                        }
                        bsync_json_str = json.dumps(bsync_json_obj)
                        Sender.send(data_json_obj['ip_address'], bsync_json_str, port)

                    # Send block to request node
                    else:
                        for root, dirs, files in os.walk(FileController.block_storage_path):
                            for file in files:
                                if file <= data_json_obj['last_file']:
                                    continue
                                # send block
                                else:
                                    f = open(FileController.block_storage_path + file, 'r')
                                    msg = f.read()
                                    write_file = {
                                        'type': 'BSYNC',
                                        'file_name': file,
                                        'message': msg
                                    }
                                    f.close()
                                    datas = json.dumps(write_file)
                                    Sender.send(data_json_obj['ip_address'], datas, port)

                        bcomplete_json_obj = {
                            'type': 'CBSYNC'
                        }
                        bcomplete_json_str = json.dumps(bcomplete_json_obj)
                        Sender.send(data_json_obj['ip_address'], bcomplete_json_str, port)
                        break

            except:
                traceback.print_exc()
                break

    tcp_socket.close()
    receive_socket.close()
