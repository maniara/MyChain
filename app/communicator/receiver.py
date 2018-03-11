import traceback
from socket import *

from app import log
from app import transaction
from app.block import validate_block, Block
from app import block
from app.transaction import Transaction
from app.node import key

is_running = True


# 수신 스레드 정지
def stop():
	global is_running
	is_running = False


#리스너를 시작하는 함수
def start(thread_name, ip_address, port):
	import json

	addr = (ip_address, port)
	buf_size = 1024

	# 소켓 생성 및 바인딩
	tcp_socket = socket(AF_INET, SOCK_STREAM)
	tcp_socket.bind(addr)
	tcp_socket.listen(5)

	while is_running:

		# 요청이 있을 경우 소켓과 송신자의 ip 주소 저장
		receive_socket, sender_ip = tcp_socket.accept()

		while is_running:
			log.write("Receiving")

			# 소켓으로부터 버퍼 사이즈씩 데이터 수신
			data = receive_socket.recv(buf_size)
			try:

				# 수신된 데이터가 없는 경우
				if len(data) == 0:
					break

				# json 형태의 데이터를 dict 타입으로 변경
				data_json_obj = json.loads(data)

				# Transaction을 받은 경우
				if data_json_obj['type'] == 'T':
					log.write("Receiving a transaction")

					# dict 데이터로부터 transaction 객체 생성
					tx = Transaction().from_json(data_json_obj)

					message = data_json_obj['time_stamp'] + data_json_obj['message']
					#트랜잭션 검증(서명 검증)
					if transaction.validate_tx(data_json_obj['pub_key'], data_json_obj['signature'], message):
						log.write("Transaction is valid")
						tx = Transaction().from_json(data_json_obj)
						transaction.add_transaction(tx)
						break
					else:
						log.write("Transaction is invalid")
						break


				# 블록을 수신한 경우
				elif data_json_obj['type'] == 'B':
					log.write("Receiving a block")
					# 블록 생성
					received_block = Block().from_json(data_json_obj)
					#블록 검증(nonce 검증)
					if validate_block(received_block):
						# 기존의 트랜잭션 삭제
						transaction.remove_all()

						# 블록 저장
						block.store_block(received_block)
						print("Block is added")
						break

					else:
						print("Block is invalid")
						break

			except:
				traceback.print_exc()
				break

	tcp_socket.close()
	receive_socket.close()
