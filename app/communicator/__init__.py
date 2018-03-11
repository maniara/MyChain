import socket
import threading
import time

import zmq

from app import log
from app.node import Node
from app import node

PING_PORT_NUMBER = 9999
PING_MSG_SIZE = 1
PING_INTERVAL = 5  # Once per second

is_running = True
t = None


# 노드 검색 스레드 정지
def stop():
	global is_running, t
	is_running = False
	t.join()


#노드를 구성하는 함수, 프라이빗인 경우 아이피 주소를 리스트로 받음
def set_network(ip_list, isPrivate = True):
	if isPrivate:
		node.remove_all_node()
		# 프라이빗 블록체인에서는 등록된 ip만 브로드캐스팅 할 수 있게함
		for ip in ip_list:
			node.add_node(Node(ip))
			#print(ip)
	else:
		start_public()


#퍼블릭 노드 생성 (생략 가능)
def start_public():
	# UDP 네트워크 내에서 모든 이 메소드를 호출하는 PC를 자동으로 노드로 등록함
	def find_node_thread():

		# UDP 소켓 생성
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

		# 소켓에 브로드캐스트 옵션 설정
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

		# 포트 번호와 로컬 주소에 바인딩
		sock.bind(('', PING_PORT_NUMBER))

		# zmq라이브러리를 이용해 UDP 소켓을 폴링
		poller = zmq.Poller()
		poller.register(sock, zmq.POLLIN)

		# 실행 시 ping 전송
		ping_at = time.time()

		while is_running:
			# 타이머 설정
			timeout = ping_at - time.time()
			if timeout < 0:
				timeout = 0
			try:
				events = dict(poller.poll(1000 * timeout))
			except KeyboardInterrupt:
				log.write("interrupted")
				break

			# ping 으로부터 응답이 오는 경우 노드 추가
			if sock.fileno() in events:
				msg, addrinfo = sock.recvfrom(PING_MSG_SIZE)
				ip = addrinfo[0]
				n = node.Node(ip)
				node.add_node(n)

			# 일정 주기 마다 브로드캐스트로 ping
			if time.time() >= ping_at:
				sock.sendto(b'!', 0, ("255.255.255.255", PING_PORT_NUMBER))
				ping_at = time.time() + PING_INTERVAL

	global t
	t = threading.Thread(target=find_node_thread)
	t.start()
