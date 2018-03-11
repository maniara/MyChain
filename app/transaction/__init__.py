import codecs
from app.transaction.Transaction import Transaction
from app.node import key

# import key
from app import storage
from app.communicator import sender

def add_transaction(tx):
	storage.insert(tx)


def get_transactions():
	return storage.get_all(Transaction)


def count():
	return storage.count(Transaction)


def remove_all():
	storage.remove_all(Transaction)


#트랜잭션 객체를 생성하는 함수
def create_tx(msg):
	tx = Transaction()
	tx.message = msg

	msg = tx.time_stamp.strftime('%Y%m%d%H%M%S') + msg

	# transaction에 공개키 저장
	tx.pub_key = codecs.encode(key.get_pub_key_string(), 'hex_codec').decode('utf-8')

	sig = key.get_signature(msg)

	# transaction에 암호화된 메세지 저장
	tx.signature = codecs.encode(sig, 'hex_codec').decode('utf-8')

	return tx


def send_tx(tx):
	# 모든 노드에 transaction 전송
	sender.send_to_all_node(tx.to_json())


#트랜잭션을 검증하는 함수
def validate_tx(pub_key, signature, message):
	#전자서명을 검증함
	if key.verify_signature(pub_key, signature, message):
		return True
