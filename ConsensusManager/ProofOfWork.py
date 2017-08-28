import hashlib
import random

from numpy import long

max_nonce = 2 ** 32


def proof_of_work(block_info, diff_bits):

    target = 2 ** (256 - diff_bits)

    found = False

    while not found:
        nonce = random.randint(0, max_nonce)

        hash_result = hashlib.sha256(str(block_info).encode('utf-8') + str(nonce).encode('utf-8')).hexdigest()

        if long(hash_result, 16) <= target:
            found = True

            return hash_result, nonce

    return nonce


if __name__ == '__main__':
    n = proof_of_work('TEST', 20)
    print(n)
