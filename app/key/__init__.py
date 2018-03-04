import os

from ecdsa import SigningKey, NIST256p, VerifyingKey

KEY_PATH = os.getcwd()


def generate_key():
	# 공개키, 개인키 생성
	pri_key = SigningKey.generate(curve=NIST256p)
	pub_key = pri_key.get_verifying_key()

	# 생성된 공인키, 개인키를 파일로 생성
	open(KEY_PATH + "/private.pem", "w", encoding='utf-8').write(pri_key.to_pem().decode('utf-8'))
	open(KEY_PATH + "/public.pem", "w", encoding='utf-8').write(pub_key.to_pem().decode('utf-8'))

	return pri_key, pub_key


def get_key():
	# 파일로부터 읽어들인 공개키, 개인키 리턴
	pri_key = SigningKey.from_pem(open(KEY_PATH + "/private.pem", encoding='utf-8').read())
	pub_key = pri_key.get_verifying_key()

	return pri_key, pub_key


def key_to_string(pub_key):
	return pub_key.to_string()


def get_signature(message, private_key):
	return private_key.sign(message.encode('utf-8'))


# public_key_str -> json object KEY: [pub_key]  type: string
def verify_signature(public_key_str, signature, message):
	public_key = VerifyingKey.from_string(bytes.fromhex(public_key_str), curve=NIST256p)
	return public_key.verify(bytes.fromhex(signature), message.encode('utf-8'))


if __name__ == '__main__':
	import json

	pri, pub = generate_key()
	pri2, pub2 = get_key()
	pub_str = pub2.to_string()

	msg1 = "\"20170121012122\""
	msg2 = "\"6fc79a615d8db9f2be77aef85f93326ccfa7758701ce741a25b22f4a\""
	msg = msg1 + msg2
	sig = get_signature(msg, pri2)

	sig2 = sig.encode('string_escape')
	pub_str = pub_str.encode('string_escape')

	test_json_obj = {
		'sig': sig2,
		'pub': pub_str
	}

	test_json_str = json.dumps(test_json_obj)
	print("JSON STR", test_json_str)

	json_obj = json.loads(test_json_str)

	print(json_obj['sig'], json_obj['pub'])

	recv_sig = json_obj['sig'].decode('string_escape')
	recv_pub = json_obj['pub'].decode('string_escape')

	print(recv_sig, recv_pub)

	veri = verify_signature(recv_pub, recv_sig, msg)

	print(veri, type(sig))
