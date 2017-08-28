import time
from FINOChainController import Property


class Block(object):
    def __init__(self, prev_block_id, prev_block_hash, tx_list, merkle_root, nonce, block_info):
        self.type = 'B'
        self.prev_block_id = prev_block_id
        self.prev_block_hash = prev_block_hash
        self.tx_list = tx_list
        self.merkle_root = merkle_root
        self.time_stamp = time.strftime('%Y%m%d%H%M%S', time.localtime())
        self.block_id = "B" + self.time_stamp
        self.block_hash = ''
        self.nonce = nonce
        self.block_info = block_info
        self.block_miner = Property.peer_number


class GenesisBlock(object):
    def __init__(self):
        self.type = 'B'
        self.prev_block_id = 'B000000000000'
        self.prev_block_hash = 'block_hash'
        self.tx_list = 'sechain'
        self.timp_stamp = '0000-00-00-00-00-00'
        self.block_id = 'B000000000000'
        self.merkle_root = 'sogangfinotek2017'
        self.block_hash = 'sechainfinochain2017'
        self.nonce = 2010101010


if __name__ == '__main__':
    import json
    t = GenesisBlock()
    temp = json.dumps(t, indent=4, default=lambda o: o.__dict__, sort_keys=True)
    temps = json.loads(temp)
    print(type(temps['nonce']))
