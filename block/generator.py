import time

import transaction
from block import Block, get_last_block, create_block
from consensus import merkle_tree
from consensus import pow


def generate_block():
    start_time = time.time()

    transactions = transaction.get_transactions()

    last_block_id, last_block = get_last_block()

    merkle_root = merkle_tree.merkle_tree(transactions)

    block_info = merkle_root + last_block.block_hash

    hash_result, nonce = pow.proof_of_work(block_info, diff_bits=5)

    block = Block(last_block_id, last_block.block_hash, transactions, merkle_root, nonce, block_info)
    block_hash = hash_result
    block.block_hash = block_hash

    create_block(block=block)

    end_time = time.time()

    print("elapsed_time: ", end_time - start_time)

    transaction.remove_all()

    # TODO
    # Sender.send_to_all_node(block_json_str)


def create_genisis_block():
    g = Block(
        prev_block_id='B000000000000',
        prev_block_hash='block_hash',
        tx_list='sechain',
        merkle_root='sogangfinotek2017',
        block_info='33333',
        nonce=2010101010)
    g.block_hash = 'sechainfinochain2017'
    create_block(block=g)


# ======================================================================================================================
if __name__ == '__main__':
    create_genisis_block()
