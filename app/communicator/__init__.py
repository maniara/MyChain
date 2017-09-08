import socket
import threading
import time

import zmq

from app import log
from app import node

PING_PORT_NUMBER = 9999
PING_MSG_SIZE = 1
PING_INTERVAL = 5  # Once per second

is_running = True
t = None


def stop():
	global is_running, t
	is_running = False
	t.join()


def start():
	def find_node_thread():

		# Create UDP socket
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

		# Ask operating system to let us do broadcasts from socket
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

		# Bind UDP socket to local port so we can receive pings
		sock.bind(('', PING_PORT_NUMBER))

		# main ping loop
		# We use zmq_poll to wait for activity on the UDP socket, since
		# this function works on non-0MQ file handles. We send a beacon
		# once a second, and we collect and report beacons that come in
		# from other nodes:
		poller = zmq.Poller()
		poller.register(sock, zmq.POLLIN)

		# Send first ping right away
		ping_at = time.time()

		while is_running:
			timeout = ping_at - time.time()
			if timeout < 0:
				timeout = 0
			try:
				events = dict(poller.poll(1000 * timeout))
			except KeyboardInterrupt:
				log.write("interrupted")
				break

			# Someone answered our ping
			if sock.fileno() in events:
				msg, addrinfo = sock.recvfrom(PING_MSG_SIZE)
				ip = addrinfo[0]
				n = node.Node(ip)
				if node.add_node(n):
					log.write('Find ' + ip)

			if time.time() >= ping_at:
				sock.sendto(b'!', 0, ("255.255.255.255", PING_PORT_NUMBER))
				ping_at = time.time() + PING_INTERVAL

	global t
	t = threading.Thread(target=find_node_thread)
	t.start()
