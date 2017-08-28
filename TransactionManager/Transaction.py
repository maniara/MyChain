import codecs
import time


class Transaction(object):
    def __init__(self, recv_addr, message):
        self.type = 'T'
        self.time_stamp = time.strftime('%Y%m%d%H%M%S', time.localtime())
        self.tx_id = self.type + self.time_stamp
        self.pub_key = ''
        self.recv_addr = recv_addr
        self.message = message  # document hash
        self.signature = ''

    def to_dict(self):
        return {
            "type": self.type,
            "time_stamp": self.time_stamp,
            "tx_id": self.tx_id,
	        "pub_key": (self.pub_key.to_string()).hex(),
            "recv_addr": self.recv_addr,
            "message": self.message,
	        "signature": codecs.encode(self.signature, 'hex_codec').decode('utf-8'),
        }
