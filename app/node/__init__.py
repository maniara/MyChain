import json

from sqlalchemy import Column, String

from app import storage


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


def remove_node(ip_address):
	target_node = storage.get(Node, ip_address=ip_address)
	storage.remove(target_node)


def add_node(node):
	filters = (
		Node.ip_address == node.ip_address
	)
	return storage.insert_or_update(node, filters)


def count():
	return storage.count(Node)


def get_my_node():
	pass


def get_all():
	return storage.get_all(Node)
