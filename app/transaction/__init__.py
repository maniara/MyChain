import codecs
from app.transaction.Transaction import Transaction

# import key
from app import storage, key
from app.communicator import sender

def add_transaction(tx):
	storage.insert(tx)


def get_transactions():
	return storage.get_all(Transaction)


def count():
	return storage.count(Transaction)


def remove_all():
	storage.remove_all(Transaction)


def create_tx(pub_key, pri_key, msg):
	tx = Transaction()
	tx.message = msg

	msg = tx.time_stamp.strftime('%Y%m%d%H%M%S') + msg

	pub_key_b = key.key_to_string(pub_key)

	# transaction에 공개키 저장
	tx.pub_key = codecs.encode(pub_key_b, 'hex_codec').decode('utf-8')

	sig = key.get_signature(msg, pri_key)

	# transaction에 암호화된 메세지 저장
	tx.signature = codecs.encode(sig, 'hex_codec').decode('utf-8')

	return tx


def send_tx(tx):
	# 모든 노드에 transaction 전송
	sender.send_to_all_node(tx.to_json())
