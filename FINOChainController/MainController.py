import threading

from CommunicationManager import Receiver
from FINOChainController import Property
from FINOChainController.FunctionAPIs import send_tx
from NodeManager import NodeController, KeyController
from StorageManager import FileController


class MainController(object):

    def __init__(self):
        return 0


    '''
        INIT NODE.
        Block sync -> Node sync -> start receiver.
    '''
    @staticmethod
    def initiate_node(*args):
        # BlockGenerator.genisis_block()
        MainController.set_my_node()

        # Block Sync
        # BlockSynchronizer.request_block_sync()

        # Node Sync
        # NodeSynchronizer.download_node_list(Property.my_node)

        # while (True):
        #     print "CHECK NODE_-------------------------------------------------"
        #     if (Property.node_sync == True):
        #         break

        '''
            For test
            peer_number = 1
            Normal Node = peer_number = 2, 3, 4, ...
        '''
        MainController.set_peer_number()

        # Start node
        MainController.start_node()
        #Property.ui_frame.write_log("Start FINO-chain")

    '''
        Start Receiver Thread
        PORT: 10654
    '''
    @staticmethod
    def start_node():
        Property.node_list = FileController.get_node_list()
        #
        # if Property.my_ip_address != Property.trust_node_ip:
        #     NodeController.send_my_node(Property.my_ip_address)
        t = threading.Thread(target=Receiver.start, args=("Listener_Thread", Property.my_ip_address, Property.port))
        t.start()

        Property.node_started = True

    @staticmethod
    def set_my_node():

        key_path = FileController.key_path + 'private.pem'

        try:
            f = open(key_path, encoding='utf-8')
            f.close()
            pri_key, pub_key = KeyController.get_key()

        except:
            pri_key, pub_key = KeyController.generate_key()

        Property.my_node, Property.my_node_json = NodeController.get_node()
        Property.private_key = pri_key
        Property.public_key = pub_key

        print(Property.private_key, Property.public_key)

        NodeController.add_new_node(Property.my_node)

    @staticmethod
    def get_ip_address():
        def get_ip_address(ifname):
            import netifaces as ni
            ni.ifaddresses(ifname)
            return ni.ifaddresses(ifname)[ni.AF_INET][0]['addr']

        Property.my_ip_address = get_ip_address('en0')

        return Property.my_ip_address

    @staticmethod
    def set_peer_number():
        if Property.my_ip_address == '203.234.223.57':
            Property.peer_number = 1

        elif Property.my_ip_address == '203.234.223.191':
            Property.peer_number = 2



MainController.get_ip_address()
MainController.initiate_node()
send_tx(Property.my_ip_address, 'sadfadsf')
