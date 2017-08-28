import hashlib

from numpy import long

from StorageManager import FileController


def vote_delegated_node():

    transactions = FileController.get_transaction_list()
    current_mk_root = hashlib.sha256(transactions[0].encode('utf-8')).hexdigest()
    # MerkleTree.merkle_tree(transactions)

    delegated_node = (long(current_mk_root, 16) % 5) + 1

    return delegated_node


def block_gen_signal():
    gen_signal = False
    vote_count = len(FileController.get_vote_count())
    node_count = len(FileController.get_node_list())

    # except node itself
    if vote_count == node_count:
        gen_signal = True

    return gen_signal


def get_vote_result(delegated_number):
    vote_list = FileController.read_all_line(FileController.database_path + FileController.vote_file)
    current_node_count = len(FileController.get_node_list())
    count = 0
    result = 0
    dele_num_str = str(delegated_number)

    for iter in vote_list:
        if dele_num_str in iter:
            count += 1

    if count >= (current_node_count / 2):
        result = delegated_number

    return result




#================ MODULE TEST===================
if __name__ == '__main__':
    r = get_vote_result(1)
    print(r)
