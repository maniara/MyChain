
def get_ip_address(ifname):
	import netifaces as ni
	ni.ifaddresses(ifname)
	return ni.ifaddresses(ifname)[ni.AF_INET][0]['addr']
