import threading
from socket import *

from app import node
from app.communicator import my_ip_address


#특정 아이피로 메시지를 전송하는 함수
def send(ip_address, message, port, *args):
	receiver_addr = (ip_address, port)
	tcp_socket = socket(AF_INET, SOCK_STREAM)
	try:
		tcp_socket.connect(receiver_addr)
		tcp_socket.send(message.encode('utf-8'))
	except Exception as e:
		print("Connection Failed while sending", e)


#모든 등록된 ip로 메시지를 전송하는 함수
def send_to_all_node(message, except_my_node=False):
	# node 목록에서 ip 만 리스트로 추출
	address_list = list(map(lambda x: x.ip_address, node.get_all()))

	# True 일 경우 내 node를 제외한 node에게 전송
	if except_my_node:
		address_list = list(filter(lambda x: x != my_ip_address.get_ip_address('en0'), address_list))

	send_threads = []

	for addr in address_list:
		try:
			# 메세지를 전송하는 스레드 생성 및 실행
			t = threading.Thread(target=send, kwargs={'ip_address': addr,
			                                          'message': message,
			                                          'port': 3000})
			t.start()
			send_threads.append(t)
		except Exception as e:
			print("SENDTOALL EXCEPT", e)

	# 스레드 객체를 배열로 저장해둔 후 동기화
	for thread in send_threads:
		thread.join()
