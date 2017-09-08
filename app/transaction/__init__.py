import datetime
import json

from dateutil import parser
from sqlalchemy import Column, String, Integer, DateTime

# import key
from app import storage
from app.communicator import sender


class Transaction(storage.Base):
	__tablename__ = 'transactions'

	_id = Column(Integer, primary_key=True, autoincrement=True)
	type = Column(String)
	time_stamp = Column(DateTime)
	tx_id = Column(String)
	pub_key = Column(String)
	message = Column(String)  # document hash
	signature = Column(String)

	def __init__(self):
		self.type = 'T'
		self.time_stamp = datetime.datetime.now()
		self.tx_id = self.type + self.time_stamp.strftime('%Y%m%d%H%M%S')
		self.pub_key = ''
		self.message = ''  # document hash
		self.signature = ''

	def __str__(self):
		return self.to_json()

	def from_json(self, dictionary):
		"""Constructor"""
		for key in dictionary:
			setattr(self, key, dictionary[key])

		self.time_stamp = parser.parse(self.time_stamp)
		return self

	def to_json(self):
		return json.dumps({
			'type': self.type,
			'time_stamp': self.time_stamp.strftime('%Y%m%d%H%M%S'),
			'tx_id': self.tx_id,
			'pub_key': self.pub_key,
			'message': self.message,
			'signature': self.signature
		})


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

	# TODO release comment when pki is implemented
	# pub_key_b = key.key_to_string(pub_key)
	# tx.pub_key = codecs.encode(pub_key_b, 'hex_codec').decode('utf-8')
	# sig = key.get_signature(msg, pri_key)

	sig = msg
	tx.signature = sig
	# codecs.encode(sig, 'hex_codec').decode('utf-8')

	return tx


def send_tx(tx):
	# 모든 노드에 transaction 전송
	sender.send_to_all_node(tx.to_json())
