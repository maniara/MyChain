import datetime
import json

from dateutil import parser
from sqlalchemy import Column, String, Integer, DateTime

# import key
from app import storage

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