import codecs
import logging

import block
import db
import log
import node
import transaction
import util
from key import get_key, generate_key
from node import Node

db.init()


class MainController(object):
	def __init__(self):
		return 0

	'''
        INIT NODE.
        Block sync -> Node sync -> start receiver.
    '''

	@staticmethod
	def initiate_node(*args):
		MainController.set_my_node()

		log.write("Start node")
		MainController.start_node()

	'''
        Start Receiver Thread
        PORT: 10654
    '''

	@staticmethod
	def start_node():
		from p2p import Receiver

		node_list = node.get_all()

		import threading
		threading.Thread(target=Receiver.start, args=("Listener_Thread",
		                                              util.get_ip_address('en0'), 3000)).start()

	@staticmethod
	def list_all_node():
		for n in node.get_all():
			log.write(n, logging.DEBUG)

	@staticmethod
	def list_all_transaction():
		for t in transaction.get_transactions():
			log.write(t, logging.DEBUG)

	@staticmethod
	def list_all_block():
		for b in block.get_all_block():
			log.write(b, logging.DEBUG)

	@staticmethod
	def set_my_node():
		key_path = '../private.pem'
		pri_key = ''
		pub_key = ''
		try:
			f = open(key_path, encoding='utf-8')
			f.close()
			pri_key, pub_key = get_key()

		except:
			pri_key, pub_key = generate_key()

		my_node = Node(util.get_ip_address('en0'))
		my_node.public_key = codecs.encode(pub_key.to_string(), 'hex_codec').decode('utf-8')
		my_node.private_key = codecs.encode(pri_key.to_string(), 'hex_codec').decode('utf-8')
		log.write("Set my node")

		node.add_node(my_node)
