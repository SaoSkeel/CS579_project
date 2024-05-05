import random
from synchronous import RC4_Synchronous
import threading

class RC4_Asynchronous:
    def __init__(self, key):
        self.key = key

    def encrypt(self, plaintext, block_size=1):
        num_blocks = (len(plaintext) + block_size - 1) // block_size
        # get Initilization Vectors
        self.ivs = self.getIV(num_blocks)
        self.new_keys = [self.key + iv for iv in self.ivs]
        self.broken_plaintext = [plaintext[i:min(i+block_size, len(plaintext))] for i in range(0, len(plaintext), block_size)]
        assert len(self.new_keys) == len(self.broken_plaintext)
        
        self.outputs = [(bytes(0),bytes(0)) for _ in range(num_blocks)]
        
        threads = [threading.Thread(target=self.runParallelEncryption, args=(i,)) for i in range(num_blocks)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        
        return self.outputs
    
    def runParallelEncryption(self, i):
        cipher = RC4_Synchronous(self.new_keys[i])
        encrypted = cipher.encrypt(self.broken_plaintext[i])
        # print(f'running thread {i}, iv: {self.ivs[i].hex()}, key: {self.new_keys[i].hex()}, plaintext: {self.broken_plaintext[i].hex()}, encrypted: {encrypted.hex()}')
        self.outputs[i] = (self.ivs[i], encrypted)
        
    
    def getIV(self, n):
        random.seed(43)
        return [random.randbytes(10) for _ in range(n)]

    def decrypt(self, ciphertexts):
        num_blocks = len(ciphertexts)
        # print(num_blocks)
        self.new_keys = [self.key + iv for iv, _ in ciphertexts]
        self.broken_plaintext = [c for _, c in ciphertexts]
        self.outputs = [(bytes(0),bytes(0)) for _ in range(num_blocks)]
        threads = [threading.Thread(target=self.runParallelEncryption, args=(i,)) for i in range(num_blocks)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return b''.join([c for _, c in self.outputs])


def main():
    key = b"SecretKey"
    rc4 = RC4_Asynchronous(key)
    plaintext = b"Hello, World!Hello, World!Hello, World!Hello, World!Hello, World!Hello, World!Hello, World!Hello, World!"
    encrypted = rc4.encrypt(plaintext, block_size=10)
    decrypted = rc4.decrypt(encrypted)
    print("Plaintext:", plaintext)
    print(f"Encrypted: text - {','.join([e.hex() for _, e in encrypted])}, ivs - {','.join([i.hex() for i, _ in encrypted])}")
    print("Decrypted:", decrypted.hex())
    # convert bytes to string
    decrypted = decrypted.decode("utf-8")
    print("Decrypted string:", decrypted)
    assert len(plaintext) == len(decrypted)

if __name__ == "__main__":
    main()
