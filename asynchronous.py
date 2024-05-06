import numpy as np
from synchronous import RC4_Synchronous
import random
import time
from multiprocessing import Process, Manager

class RC4_Asynchronous:
    def __init__(self, key):
        """
        Initialize the RC4_Asynchronous class.

        Args:
            key (bytes): The key for encryption and decryption.
        """
        self.key = key

    def encrypt(self, plaintext, block_size=1, measure_time=False):
        """
        Encrypt the plaintext asynchronously.

        Args:
            plaintext (bytes): The plaintext to be encrypted.
            block_size (int): The size of each block for encryption.

        Returns:
            np.ndarray: An array containing tuples of (IV, encrypted_text).
        """
        num_blocks = (len(plaintext) + block_size - 1) // block_size
        # debug
        # print(num_blocks)

        # Generate Initialization Vectors (IVs)
        self.ivs = self.getIV(num_blocks)

        # Generate new keys based on IVs
        self.new_keys = np.array([self.key + iv for iv in self.ivs])

        # Break plaintext into blocks
        self.broken_plaintext = np.array([
            plaintext[i:min(i + block_size, len(plaintext))]
            for i in range(0, len(plaintext), block_size)
        ])
        assert len(self.new_keys) == len(self.broken_plaintext)

        # Initialize an array to store outputs
        # self.outputs = np.empty(num_blocks, dtype=object)
        a = [[bytes(0), bytes(0)]] * num_blocks
        for i in range(num_blocks):
            a[i] = [self.ivs[i],bytes(0)]
        outputs = Manager().list(a)

        start_time, end_time = 0, 0
        if measure_time:
            start_time = time.time()
        threads = [Process(target=self.runParallelEncryption, args=(i,self.new_keys[i], self.broken_plaintext[i], outputs)) for i in range(num_blocks)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        if measure_time:
            end_time = time.time()
        
        return list(outputs), end_time - start_time

    def runParallelEncryption(self, i, key, plaintext, outputs):
        """
        Run encryption for a single block in parallel.

        Args:
            i (int): Index of the block to be encrypted.
        """
        cipher = RC4_Synchronous(key)
        encrypted = cipher.encrypt(plaintext)
        outputs[i][1] = encrypted

    def getIV(self, n):
        """
        Generate Initialization Vectors (IVs).

        Args:
            n (int): Number of IVs to generate.

        Returns:
            list: List of randomly generated IVs.
        """
        random.seed(43)
        return [random.randbytes(10) for _ in range(n)]

    def decrypt(self, ciphertexts, measure_time=False):
        """
        Decrypt the ciphertexts asynchronously.

        Args:
            ciphertexts (np.ndarray): An array containing tuples of (IV, ciphertext).

        Returns:
            bytes: The decrypted plaintext.
        """
        num_blocks = len(ciphertexts)

        # Generate new keys based on IVs
        self.new_keys = np.array([self.key + iv for iv, _ in ciphertexts])

        # Extract ciphertexts from input
        self.broken_ciphertexts = np.array([c for _, c in ciphertexts])

        # Initialize an array to store outputs
        a = [[bytes(0), bytes(0)]] * num_blocks
        for i in range(num_blocks):
            a[i] = [self.ivs[i],bytes(0)]
        outputs = Manager().list(a)
        
        start_time, end_time = 0, 0
        if measure_time:
            start_time = time.time()
        threads = [Process(target=self.runParallelEncryption, args=(i,self.new_keys[i], self.broken_plaintext[i], outputs)) for i in range(num_blocks)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        if measure_time:
            end_time = time.time()

        return b''.join([c for _, c in outputs]), end_time - start_time

    def runParallelDecryption(self, i, key, ciphertext, outputs):
        """
        Run decryption for a single block in parallel.

        Args:
            i (int): Index of the block to be decrypted.
        """
        cipher = RC4_Synchronous(key)
        decrypted = cipher.decrypt(ciphertext)
        outputs[i][1] = decrypted

def main():
    key = b"SecretKey"
    rc4 = RC4_Asynchronous(key)
    plaintext = b"Hello, World!"
    encrypted, _ = rc4.encrypt(plaintext, block_size=10, measure_time=False)
    decrypted, _ = rc4.decrypt(encrypted)
    print("Plaintext:", plaintext)
    print(
        f"Encrypted: text - {','.join([e.hex() for _, e in encrypted])}, ivs - {','.join([i.hex() for i, _ in encrypted])}")
    print("Decrypted:", decrypted.hex())
    # convert bytes to string
    decrypted = decrypted.decode("utf-8")
    print("Decrypted string:", decrypted)
    assert len(plaintext) == len(decrypted)

if __name__ == "__main__":
    main()
