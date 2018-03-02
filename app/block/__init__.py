import json
from app import storage
from app.block.Block import Block
from app.block.GenesisBlock import GenesisBlock

def create_block(block):
    storage.insert(block)


def get_my_block():
    return 0


def count():
    return storage.count(Block)


def get_all_block():
    return storage.get_all(Block)


def get_genesis_block():
    b = Block()
    b.prev_block_id = 'B000000000000'
    b.prev_block_hash = '0'
    b.block_id = 'B000000000000'
    b.merkle_root = 'mychain'
    b.block_hash = 'mychain'
    b.nonce = 2010101010

    return b


def get_last_block():
    if count() == 0:
        return get_genesis_block()
    else:
        return get_all_block()[-1]


if __name__ == '__main__':

    t = GenesisBlock()
    temp = json.dumps(t, indent=4, default=lambda o: o.__dict__, sort_keys=True)
    temps = json.loads(temp)
    print(type(temps['nonce']))
