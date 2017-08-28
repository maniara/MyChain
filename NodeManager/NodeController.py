from FINOChainController import Property
from NodeManager import Node, JsonEncoder
from StorageManager import FileController

import json


def get_node():


    if FileController.get_node() is False:

        new_node = Node.Node(Property.my_ip_address)

        node_json_obj = {
            'type': new_node.type,
            'ip_address': new_node.ip_address
        }

        node_json_str = json.dumps(node_json_obj, cls=JsonEncoder.json_encoder)

        FileController.add_node_info(node_json_str)

        return node_json_obj, node_json_str

    else:
        my_node = FileController.get_node()
        load_my_node = json.loads(my_node)

        # JSON Object, JSON String
        return load_my_node, my_node


def send_my_node(ip_address):
    from CommunicationManager import Sender

    mynode_json_obj = {
        'type': 'N',
        'ip_address': ip_address
    }

    mynode_json_str = json.dumps(mynode_json_obj)
    Sender.send_to_all_node(mynode_json_str)


def add_new_node(node_json_obj):
    sync_flag = False
    node_list = FileController.get_node_list()

    if len(node_list) == 0 :
        FileController.add_node_info(json.dumps(node_json_obj))

    else:
        for outer_list in node_list:
            outer_list = str(outer_list)
            if outer_list in node_json_obj['ip_address']:
                sync_flag = True

        if sync_flag is False:
            if Property.my_ip_address != node_json_obj['ip_address']:
                FileController.add_node_info(json.dumps(node_json_obj))
                Property.ui_frame.write_log("New Node is connected")
        else:
            Property.ui_frame.write_log("Already connected")
