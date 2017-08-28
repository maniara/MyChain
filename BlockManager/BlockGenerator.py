import hashlib
import json
import time

from BlockManager import Block
from CommunicationManager import Sender
from ConsensusManager import ProofOfWork
from StorageManager import FileController


def generate_block():
    start_time = time.time()

    transactions = FileController.get_transaction_list()
    # transactions.append(last_transaction + "\n")

    if len(transactions) == 0:
        return

    last_block_id, last_block = FileController.get_last_block()
    #last_block_hash = hashlib.sha256(last_block).hexdigest()

    last_block_jobj = json.loads(last_block)

    # merkle_root = MerkleTree.merkle_tree(transactions)
    merkle_root = hashlib.sha256(transactions[0].encode('utf-8')).hexdigest()
    block_info = merkle_root + last_block_jobj['block_hash']

    hash_result, nonce = ProofOfWork.proof_of_work(block_info, diff_bits=5)

    block = Block.Block(last_block_id, last_block_jobj['block_hash'], transactions, merkle_root, nonce, block_info)
    block_hash = hash_result
    block.block_hash = block_hash

    block_json_str = json.dumps(block, indent=4, default=lambda o: o.__dict__, sort_keys=True)
    FileController.create_new_block(block.block_id, block_json_str)
    end_time = time.time()

    print("elapsed_time: ", end_time - start_time)

    # FileController.remove_all_transactions()


    Sender.send_to_all_node(block_json_str)


def genisis_block():

    block_id = 'B000000000000'
    block = Block.GenesisBlock()
    genblock_json_str = json.dumps(block, indent=4, default=lambda o: o.__dict__, sort_keys=True)

    FileController.create_new_block(block_id, genblock_json_str)




#======================================================================================================================
if __name__ == '__main__':
    pass
    # transactions = [
    #     '{"recv_addr": "1", "tx_id": "T20170118092904", "time_stamp": "20170118092904", "pub_key": "", "type": "T", "message": "da7f6e26c3f9183399be2adb5d8ec6b9b2c211a0955a6ec8a24bc66f"}',
    #     '{"recv_addr": "2", "tx_id": "T20170118095955", "time_stamp": "20170118095955", "pub_key": "", "type": "T", "message": "1073382bc80d8cc2828f790b4ff148ae1ef145260000ebb884a15bf9"}',
    #     '{"recv_addr": "3", "tx_id": "T20170118092904", "time_stamp": "20170118092904", "pub_key": "", "type": "T", "message": "da7f6e26c3f9183399be2adb5d8ec6b9b2c211a0955a6ec8a24bc66f"}',
    #     '{"recv_addr": "4", "tx_id": "T20170118092904", "time_stamp": "20170118092904", "pub_key": "", "type": "T", "message": "da7f6e26c3f9183399be2adb5d8ec6b9b2c211a0955a6ec8a24bc66f"}',
    #     '{"recv_addr": "5", "tx_id": "T20170118092904", "time_stamp": "20170118092904", "pub_key": "", "type": "T", "message": "da7f6e26c3f9183399be2adb5d8ec6b9b2c211a0955a6ec8a24bc66f"}',
    #     '{"recv_addr": "6", "tx_id": "T20170118092904", "time_stamp": "20170118092904", "pub_key": "", "type": "T", "message": "da7f6e26c3f9183399be2adb5d8ec6b9b2c211a0955a6ec8a24bc66f"}',
    #     '{"recv_addr": "7", "tx_id": "T20170118092904", "time_stamp": "20170118092904", "pub_key": "", "type": "T", "message": "da7f6e26c3f9183399be2adb5d8ec6b9b2c211a0955a6ec8a24bc66f"}',
    #     '{"recv_addr": "8", "tx_id": "T20170118092904", "time_stamp": "20170118092904", "pub_key": "", "type": "T", "message": "da7f6e26cf9183399be2adb5d8ec6b9b2c211a0955a6ec8a24bc66f"}',
    #     '{"recv_addr": "9", "tx_id": "T20170118092904", "time_stamp": "20170118092904", "pub_key": "", "type": "T", "message": "da7f6e26c3f9183399be2adb5d8ec6b9b2c211a0955a6ec8a24bc66f"}',
    #     '{"recv_addr": "10", "tx_id": "T20170118092904", "time_stamp": "20170118092904", "pub_key": "", "type": "T", "message": "da7f6e26c3f9183399be2adb5d8ec6b9b2c211a0955a6ec8a24bc66f"}',
    #     ]
    # tx = FileController.get_transaction_list()
    # mk = MerkleTree.merkle_tree(transactions)
    #
    # block = Block.Block('B00', 'abcd', transactions, mk)
    #
    # block_json_str = json.dumps(block, indent=4, default=lambda o: o.__dict__, sort_keys=True)
    # print(block_json_str, sys.getsizeof(block_json_str))
    # genisis_block()