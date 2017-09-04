def get_ip_address(ifname):
	ni.ifaddresses(ifname)
	return ni.ifaddresses(ifname)[ni.AF_INET][0]['addr']