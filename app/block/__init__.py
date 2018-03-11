import datetime

from app import storage
from app.block.Block import Block
from app.block.merkle_tree import merkle_tree
from app.consensus import pow


#블록을 생성하는 함수
def create_block(transactions):

    # 내 node 가 가지고 있는 마지막 블럭
    last_block = get_last_block()

    # 모든 transaction을 리스트로 생성
    transactions_str = list(map(lambda x: x.to_json(), transactions))


    merkle_root = merkle_tree(transactions_str)

    # block 정보에 merkle root 할당
    block_info = merkle_root

    # block 객체 생성
    _block = Block()

    # 마지막 block이 있는 경우
    if last_block:
        # block 정보에 마지막 블럭의 해쉬를 더함
        block_info += last_block.block_hash

        # 새로 생성한 block에 이전 block 정보 저장
        _block.prev_block_hash = last_block.block_hash
        _block.prev_block_id = last_block.block_id

    # 작업 증명을 통해 nonce값과 hash 결과 생성
    hash_result, nonce = pow.get_nonce(block_info, diff_bits=5)

    # block 정보
    _block.block_hash = hash_result
    _block.nonce = nonce
    _block.block_info = block_info
    _block.time_stamp = datetime.datetime.now()
    _block.block_id = "B"+str(_block.time_stamp)
    _block.merkle_root = merkle_root

    return _block


def store_block(_block):
    # 내 node 에 block 저장
    storage.insert(_block)


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


#최종 블록 가져오기
def get_last_block():
    if count() == 0:
        #블록이 없으면 genesis block 을 생성
        return get_genesis_block()
    else:
        return get_all_block()[-1]


#블록 검증 (블록 수신후 수신한 블록을 검증하는) 함수
#nonce를 잘 찾았는지 검사
def validate_block(block):
    from numpy import long

    #check nonce
    block_info = block.block_hash
    nonce = block.nonce
    diff_bits = 5
    target = 2 ** (256 - diff_bits)

    #hash_result = hashlib.sha256(str(block_info).encode('utf-8') + str(nonce).encode('utf-8')).hexdigest()

    #print("Validating block:" + str(long(block_info,16))+"/"+str(target))

    #블록의 해시가 target 보다 작은가
    if long(block_info, 16) <= target:
        return True
    else:
        return False

