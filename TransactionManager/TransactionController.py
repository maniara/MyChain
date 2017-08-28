from NodeManager import KeyController
from TransactionManager import Transaction


def create_tx(pub_key, pri_key, recv_addr, msg):

    tx = Transaction.Transaction(recv_addr, msg)

    pub_key_str = KeyController.key_to_string(pub_key)
    tx.pub_key = pub_key

    msg = tx.time_stamp + msg

    tx.signature = KeyController.get_signature(msg, pri_key)

    return tx
