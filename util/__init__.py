import netifaces
def get_ip_address(ifname):
	netifaces.ifaddresses(ifname)
	return netifaces.ifaddresses(ifname)[netifaces.AF_INET][0]['addr']
