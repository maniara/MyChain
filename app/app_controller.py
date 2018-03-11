from app import log, storage, node, transaction, block
from app import communicator
from app.node.Node import Node
from app.communicator import receiver
from app.communicator import sender

#블록체인 컨트롤 인터페이스 API
listen_thread = None
port_number = None


def start_app(ip_list, isPrivate):
	port_number = 3000
	storage.init()
	communicator.set_network(ip_list, isPrivate)
	start_communicator(port_number)


def finish_app():
	import os
	storage.session.commit()
	storage.session.close()
	stop_communicator()
	os._exit(1)


def send_transaction(msg):
	# pri_key, pub_key = key.get_key()
	tx = transaction.create_tx(msg)
	transaction.send_tx(tx)


def start_communicator(port):
	import threading
	global port_number
	port_number = port
	set_my_node(False)
	node.key.generate_key()

	log.write("Start node")

	global listen_thread
	listen_thread = threading.Thread(target=receiver.start, args=("Listener_Thread",
																			   communicator.my_ip_address.get_ip_address('en0'), port_number))
	listen_thread.start()


def stop_communicator():
	communicator.receiver.stop()
	global listen_thread
	listen_thread.join()


def create_block():
	transactions = transaction.get_transactions()

	# transaction이 없을 경우 block을 생성하지 않음
	if len(transactions) == 0:
		return

	_block = block.create_block(transactions)

	block.store_block(_block)

	# 내 node가 가지고 있는 transaction 삭제
	transaction.remove_all()

	# 나머지 node에게 block 전송
	sender.send_to_all_node((_block.to_json()), except_my_node=True)


def list_all_node():
	for n in node.get_all():
		log.write(n, logging.DEBUG)


def list_all_transaction():
	import logging
	for t in transaction.get_transactions():
		log.write(t, logging.DEBUG)


def list_all_block():
	import logging
	for b in block.get_all_block():
		log.write(b, logging.DEBUG)


#나의 IP를 노드로 등록함
def set_my_node(set_my_node=True):
	if set_my_node:
		my_node = Node(my_ip_address.get_ip_address('en0'))
		node.add_node(my_node)
	log.write("Set my node")

