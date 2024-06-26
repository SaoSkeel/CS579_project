import time
from typing import Callable, Tuple
from synchronous import RC4_Synchronous
from asynchronous import RC4_Asynchronous
import os


def benchmark_performance_sync(rc4_constructor: Callable, key: bytes, plaintext: bytes) -> Tuple[float, float]:
    """
    Measure the encryption and decryption time of RC4 synchronously.
    """
    rc4 = rc4_constructor(key)

    start_encryption = time.time()
    encrypted = rc4.encrypt(plaintext)
    end_encryption = time.time()
    enc_time = end_encryption - start_encryption

    start_decryption = time.time()
    decrypted = rc4.decrypt(encrypted)  # Decrypting the already encrypted data
    end_decryption = time.time()
    dec_time = end_decryption - start_decryption

    return enc_time, dec_time


def benchmark_performance_async(rc4_instance: RC4_Asynchronous, plaintext: bytes, block_size: int) -> Tuple[float, float]:
    """
    Measure the encryption and decryption time of RC4 asynchronously.
    """
    # Warm-up run to let threads initialize
    rc4_instance.encrypt(plaintext, block_size)

    # Measure encryption time
    encrypted, enc_time = rc4_instance.encrypt(plaintext, block_size, measure_time=True)

    # Measure decryption time
    decrypted, dec_time = rc4_instance.decrypt(encrypted, measure_time=True)

    return enc_time, dec_time

def generate_large_input(file_path, size_in_bytes):
    with open(file_path, 'wb') as f:
        f.write(os.urandom(size_in_bytes))

def read_large_input(file_path):
    with open(file_path, 'rb') as f:
        return f.read()

if __name__ == "__main__":
    key = b"supersecretkey"

    file_path = "large_input.bin"  # Change this to desired file path
    size_in_bytes = 10 * 1024 * 1024

    generate_large_input(file_path, size_in_bytes)

    plaintext = read_large_input(file_path)

    print("Synchronous Encryption Time: 0.0")
    print("Synchronous Decryption Time: 0.0")

    enc_time_sync, dec_time_sync = benchmark_performance_sync(RC4_Synchronous, key, plaintext)
    print(f"Synchronous Encryption Time: {enc_time_sync}")
    print(f"Synchronous Decryption Time: {dec_time_sync}")

    rc4_async = RC4_Asynchronous(key)
    enc_time_async, dec_time_async = benchmark_performance_async(rc4_async, plaintext, 1024 * 1024)
    print(f"Asynchronous Encryption Time: {enc_time_async}")
    print(f"Asynchronous Decryption Time: {dec_time_async}")
