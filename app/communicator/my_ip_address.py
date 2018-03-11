import netifaces
import socket


#나의 아이피를 가져오는 함수
def get_ip_address(ifname):
	import platform
	plf = platform.system()
	#윈도우인 경우
	if plf == 'Windows':
		return ([l for l in (
			[ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [
				[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in
				 [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
	#윈도우가 아닌 경우
	else:
		netifaces.ifaddresses(ifname)
		return netifaces.ifaddresses(ifname)[netifaces.AF_INET][0]['addr']
