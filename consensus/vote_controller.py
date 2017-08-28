from numpy import long

import node
import transaction
from consensus import get_vote_count, get_votes
from consensus.merkle_tree import merkle_tree


def vote_delegated_node():
    transactions = transaction.get_transactions()
    current_mk_root = merkle_tree(transactions)

    delegated_node = (long(current_mk_root, 16) % 5) + 1

    return delegated_node


def block_gen_signal():
    gen_signal = False
    vote_count = get_vote_count()
    node_count = node.get_all()

    # except node itself
    if vote_count == node_count:
        gen_signal = True

    return gen_signal


def get_vote_result(delegated_number):
    vote_list = get_votes()

    current_node_count = node.count()
    count = 0
    result = 0
    dele_num_str = str(delegated_number)

    for iter in vote_list:
        if dele_num_str in iter:
            count += 1

    if count >= (current_node_count / 2):
        result = delegated_number

    return result


# ================ MODULE TEST===================
if __name__ == '__main__':
    r = get_vote_result(1)
    print(r)
