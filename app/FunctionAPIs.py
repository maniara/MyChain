import key
import transaction
from communicator import Sender


def send_tx(recv_addr, msg):
	pub_key, pri_key = key.get_key()
	tx = transaction.create_tx(pub_key, pri_key, recv_addr, msg)
	Sender.send_to_all_node(tx.to_json())
	transaction.add_transaction(tx)


def search_tx(tx_id):
	tx_list = transaction.get_transactions()
	return list(filter(lambda x: x.tx_id == tx_id, tx_list))[0]


def search_block_info(block_id):
	import json
	block_list = file_controller.get_local_blocklist()

	for iter in block_list:
		block_jobj = json.loads(iter)
		if block_jobj['block_id'] == block_id:
			return block_jobj

	return False


def search_hash(file_hash):
	import json
	tx_list = file_controller.get_transaction_list()

	for tx in tx_list:
		tx_json_obj = json.loads(tx)
		if tx_json_obj['message'] == file_hash:
			return True

	return False


def search_block(file_hash):
	flag = False

	block_list = file_controller.get_local_blocklist()

	for iter in block_list:
		if file_hash in iter:
			flag = True

	return flag


def test_tx():
	tx_json_str = controller.create_tx('t', 't', 't', 't')

	Sender.send_to_all_node(tx_json_str)
	file_controller.add_transaction(tx_json_str)


if __name__ == '__main__':
	f = 'd759eae31b5sa1ba01fc1fb6512a38e23b119d688e627b6c2f44aa43d'
	t = search_block_info('B20170120220318')
	print(t)
