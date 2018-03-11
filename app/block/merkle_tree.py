import codecs
import hashlib

from merkle import MerkleTree


def chunk(list, n):
    for i in range(0, len(list), n):
        yield list[i:i + n]

# 라이브러리를 사용한 머클트리
def merkle_tree(transactions):
    mt = MerkleTree()

    for t in transactions:
        mt.add(t.encode('utf-8'))

    return codecs.encode(mt.build(), 'hex-codec').decode('utf-8')


# 머클트리 직접 구현방법(생략 가능)
def merkle_tree_2(p_items):
    blocks = []

    if not p_items:
        raise ValueError('')

    for m in sorted(p_items):
        blocks.append(m)

    list_len = len(blocks)

    # make even number of items in list
    while list_len % 2 != 0:
        blocks.extend(blocks[-1:])
        list_len = len(blocks)

    secondary = []

    for k in [blocks[x:x + 2] for x in range(0, len(blocks), 2)]:
        hasher = hashlib.sha256()
        k[0] = k[0].encode('utf-8')
        k[1] = k[1].encode('utf-8')
        hasher.update(k[0] + k[1])
        secondary.append(hasher.hexdigest())

    if len(secondary) == 1:
        return secondary[0][0:64]

    # recursive
    else:
        return merkle_tree_2(secondary)


# ========================================================
if __name__ == '__main__':
    transactions = [
        '{"recv_addr": "1", "tx_id": "T20170118092904", "time_stamp": "20170118092904", "pub_key": "", "type": "T", "message": "da7f6e26c3f9183399be2adb5d8ec6b9b2c211a0955a6ec8a24bc66f"}',
        '{"recv_addr": "2", "tx_id": "T20170118095955", "time_stamp": "20170118095955", "pub_key": "", "type": "T", "message": "1073382bc80d8cc2828f790b4ff148ae1ef145260000ebb884a15bf9"}',
        '{"recv_addr": "3", "tx_id": "T20170118092904", "time_stamp": "20170118092904", "pub_key": "", "type": "T", "message": "da7f6e26c3f9183399be2adb5d8ec6b9b2c211a0955a6ec8a24bc66f"}',
        '{"recv_addr": "4", "tx_id": "T20170118092904", "time_stamp": "20170118092904", "pub_key": "", "type": "T", "message": "da7f6e26c3f9183399be2adb5d8ec6b9b2c211a0955a6ec8a24bc66f"}',
        '{"recv_addr": "5", "tx_id": "T20170118092904", "time_stamp": "20170118092904", "pub_key": "", "type": "T", "message": "da7f6e26c3f9183399be2adb5d8ec6b9b2c211a0955a6ec8a24bc66f"}',
        '{"recv_addr": "6", "tx_id": "T20170118092904", "time_stamp": "20170118092904", "pub_key": "", "type": "T", "message": "da7f6e26c3f9183399be2adb5d8ec6b9b2c211a0955a6ec8a24bc66f"}',
        '{"recv_addr": "7", "tx_id": "T20170118092904", "time_stamp": "20170118092904", "pub_key": "", "type": "T", "message": "da7f6e26c3f9183399be2adb5d8ec6b9b2c211a0955a6ec8a24bc66f"}',
        '{"recv_addr": "8", "tx_id": "T20170118092904", "time_stamp": "20170118092904", "pub_key": "", "type": "T", "message": "da7f6e26cf9183399be2adb5d8ec6b9b2c211a0955a6ec8a24bc66f"}',
        '{"recv_addr": "9", "tx_id": "T20170118092904", "time_stamp": "20170118092904", "pub_key": "", "type": "T", "message": "da7f6e26c3f9183399be2adb5d8ec6b9b2c211a0955a6ec8a24bc66f"}'
    ]

    test = merkle_tree(transactions)
    print(test)
    test = merkle_tree(test)
    print(test)
    test = merkle_tree(test)
    print(test)
    test = merkle_tree(test)
    print(test)
