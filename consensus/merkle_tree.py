import hashlib


def chunk(list, n):
    for i in range(0, len(list), n):
        yield list[i:i + n]


def merkle_tree(transactions):
    sub_tree = []

    for i in chunk(transactions, 1):
        if len(i) == 2:
            hash = hashlib.sha256(str(i[0] + i[1]).encode('utf-8')).hexdigest()
        else:
            hash = hashlib.sha256(str(i[0] + i[0]).encode('utf-8')).hexdigest()
        sub_tree.append(hash)

    if len(sub_tree) == 1:
        return sub_tree[0]
    else:
        return merkle_tree(sub_tree)

# ========================================================
if __name__ == '__main__':
    transactions = [
        '{"recv_addr": "1", "tx_id": "T20170118092904", "time_stamp": "20170118092904", "pub_key": "", "type": "T", "message": "da7f6e26c3f9183399be2adb5d8ec6b9b2c211a0955a6ec8a24bc66f"}', ]
    test = merkle_tree(transactions)
    print(test)
    test = merkle_tree(transactions)
    print(test)
    test = merkle_tree(transactions)
    print(test)
    test = merkle_tree(transactions)
    print(test)
