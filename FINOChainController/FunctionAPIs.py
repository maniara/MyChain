from CommunicationManager import Sender
from FINOChainController import Property
from StorageManager import FileController
from TransactionManager import TransactionController


def send_tx(recv_addr, msg):
    import json

    tx = TransactionController.create_tx(Property.public_key, Property.private_key, recv_addr, msg)
    tx_json_str = json.dumps(tx.to_dict())
    Property.tx_count += 1
    Sender.send(recv_addr, tx_json_str, Property.port)
    FileController.add_transaction(tx_json_str)



def search_tx(tx_id):
    import json
    tx_list = FileController.get_transaction_list()

    for tx in tx_list:
        tx_json_obj = json.loads(tx)
        if tx_json_obj['tx_id'] == tx_id:
            return tx_json_obj

    return False

def search_block_info(block_id):
    import json
    block_list = FileController.get_local_blocklist()

    for iter in block_list:
        block_jobj = json.loads(iter)
        if block_jobj['block_id'] == block_id:
            return block_jobj

    return False



def search_hash(file_hash):
    import json
    tx_list = FileController.get_transaction_list()

    for tx in tx_list:
        tx_json_obj = json.loads(tx)
        if tx_json_obj['message'] == file_hash:
            return True

    return False


def search_block(file_hash):
    flag = False

    block_list = FileController.get_local_blocklist()

    for iter in block_list:
        if file_hash in iter:
            flag = True

    return flag


def test_tx():
    tx_json_str = TransactionController.create_tx('t', 't', 't', 't')

    Sender.send_to_all_node(tx_json_str)
    FileController.add_transaction(tx_json_str)


if __name__ == '__main__':
    send_tx('203.234.223.191', 'sadfadsf')
    # f = 'd759eae31b5sa1ba01fc1fb6512a38e23b119d688e627b6c2f44aa43d'
    # t = search_block_info('B20170120220318')
    # print(t)
