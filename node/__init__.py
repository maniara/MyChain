import json

import storage
from sqlalchemy import Column, String


class Node(storage.Base):
	__tablename__ = 'nodes'

	ip_address = Column(String, primary_key=True)
	type = Column(String)
	public_key = Column(String)
	private_key = Column(String)

	def __init__(self, ip_address):
		self.type = 'N'
		self.ip_address = ip_address
		self.public_key = ''
		self.private_key = ''

	def __str__(self):
		return self.to_json()

	def to_json(self):
		return json.dumps({
			'type': self.type,
			'ip_address': self.ip_address,
			'pub_key': self.public_key,
			'pri_key': self.private_key
		})


def add_node(node):
	storage.insert_or_update(node, ip_address=node.ip_address)


def count():
	return storage.count(Node)


def get_my_node():
	pass


def get_all():
	return storage.get_all(Node)
