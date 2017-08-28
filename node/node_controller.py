import node
import util
from node import Node


def get_node():
    my_node = node.get_my_node()

    if my_node is None:
        new_node = Node(
            util.get_ip_address('en0')
        )
        node.add_node(new_node)
        return new_node

    else:
        return my_node


def send_my_node(ip_address):
    my_node = Node(
        ip_address=ip_address
    )

    # TODO
    # Sender.send_to_all_node(my_node)


def add_new_node(_node):
    sync_flag = False
    node_list = node.get_all()

    if len(node_list) == 0:
        node.add_node(_node)

    else:
        for outer_list in node_list:
            outer_list = str(outer_list)
            if outer_list in _node.ip_address:
                sync_flag = True

        if sync_flag is False:
            if Property.my_ip_address != _node.ip_address:
                node.add_node(node)
                Property.ui_frame.write_log("New Node is connected")
        else:
            Property.ui_frame.write_log("Already connected")
