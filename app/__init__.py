from app import *
from app import log, storage, node, transaction, util, key, block
from app.communicator import receiver
from app.node import Node

storage.init()
key.generate_key()

listen_thread = None


def initiate_node(*args):
	set_my_node()

	log.write("Start node")
	start_node()


'''
	Start Receiver Thread
	PORT: 10654
'''


def start_node():
	import threading
	global listen_thread
	listen_thread = threading.Thread(target=receiver.start, args=("Listener_Thread",
	                                                              util.get_ip_address('en0'), 3000))
	listen_thread.start()


def stop_node():
	storage.session.commit()
	storage.session.close()
	receiver.stop()
	global listen_thread
	listen_thread.join()

def list_all_node():
	for n in node.get_all():
		log.write(n, logging.DEBUG)


def list_all_transaction():
	for t in transaction.get_transactions():
		log.write(t, logging.DEBUG)


def list_all_block():
	for b in block.get_all_block():
		log.write(b, logging.DEBUG)


def set_my_node():
	# todo implement generating key
	'''
	key_path = '../private.pem'
	pri_key = ''
	pub_key = ''
	try:

		f = open(key_path, encoding='utf-8')
		f.close()
		pri_key, pub_key = get_key()

	except:
		pri_key, pub_key = generate_key()
	'''

	my_node = Node(util.get_ip_address('en0'))

	# my_node.public_key = codecs.encode(pub_key.to_string(), 'hex_codec').decode('utf-8')
	# my_node.private_key = codecs.encode(pri_key.to_string(), 'hex_codec').decode('utf-8')
	log.write("Set my node")
	node.add_node(my_node)
