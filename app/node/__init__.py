from app.node.Node import Node
from app import storage

def remove_node(ip_address):
	target_node = storage.get(Node, ip_address=ip_address)
	storage.remove(target_node)

def remove_all_node():
	storage.remove_all(Node)


def add_node(node):
	filters = (
		Node.ip_address == node.ip_address
	)
	return storage.insert_or_update(node, filters)


def count():
	return storage.count(Node)


def get_all():
	return storage.get_all(Node)
