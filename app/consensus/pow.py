import hashlib
import random

from numpy import long

max_nonce = 2 ** 32


def get_nonce(block_info, diff_bits):

    target = 2 ** (256 - diff_bits)

    found = False

    #target 보다 작은 해시의 nonce를 찾을 때 까지
    while not found:
        nonce = random.randint(0, max_nonce)

        hash_result = hashlib.sha256(str(block_info).encode('utf-8') + str(nonce).encode('utf-8')).hexdigest()

        if long(hash_result, 16) <= target:
            return hash_result, nonce

    return nonce


if __name__ == '__main__':
    n = get_nonce('TEST', 20)
    print(n)
