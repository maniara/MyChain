import traceback
from socket import *

from app import log
from app import node
from app import transaction
from app.block import create_block
from app.transaction import Transaction

is_running = True


def stop():
	global is_running
	is_running = False


def start(thread_name, ip_address, port):
	import json

	addr = (ip_address, port)
	buf_size = 1024

	tcp_socket = socket(AF_INET, SOCK_STREAM)
	tcp_socket.bind(addr)
	tcp_socket.listen(5)

	while is_running:

		receive_socket, sender_ip = tcp_socket.accept()

		while is_running:
			log.write("Receiving")
			data = receive_socket.recv(buf_size)
			try:

				if len(data) == 0:
					break

				data_json_obj = json.loads(data)

				if data_json_obj['type'] == 'T':
					log.write("Receiving a transaction")
					tx = Transaction().from_json(data_json_obj)
					transaction.add_transaction(tx)

					# TODO release comment when pki is implemented
					# verify_msg = data_json_obj['time_stamp'] + data_json_obj['message']
					#
					# if key.verify_signature(data_json_obj['pub_key'], data_json_obj['signature'],
					#                                         verify_msg) is True:
					#     log.write("Transaction is valid")
					#     tx = Transaction().from_json(data_json_obj)
					#     transaction.add_transaction(tx)
					# else:
					#     log.write("Transaction is invalid")

				elif data_json_obj['type'] == 'N':
					from app.node import node_controller
					log.write("Receiving Node")

					node_list = node.get_all()
					received_ip = data_json_obj['ip_address']
					sync_flag = False

					for outer_list in node_list:
						outer_list = str(outer_list)
						if outer_list == received_ip:
							sync_flag = True

					if sync_flag is False:
						node_controller.add_new_node(data_json_obj)

				# When received block, add to file database
				elif data_json_obj['type'] == 'B':
					transaction.remove_all()
					create_block(data_json_obj['block_id'], data)

			except:
				traceback.print_exc()
				break

	tcp_socket.close()
	receive_socket.close()
