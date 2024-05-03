import asyncio
import time
from typing import Callable, Tuple

from synchronous import RC4_Synchronous
from asynchronous import RC4_Asynchronous


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


async def benchmark_performance_async(rc4_instance: RC4_Asynchronous, plaintext: bytes) -> Tuple[float, float]:
    """
    Measure the encryption and decryption time of RC4 asynchronously.
    """
    start_encryption = time.time()
    encrypted = await rc4_instance.encrypt(plaintext)
    end_encryption = time.time()
    enc_time = end_encryption - start_encryption

    start_decryption = time.time()
    decrypted = await rc4_instance.decrypt(encrypted)
    end_decryption = time.time()
    dec_time = end_decryption - start_decryption

    return enc_time, dec_time


if __name__ == "__main__":
    key = b"supersecretkey"
    plaintext = b"hello world"

    print("Synchronous Encryption Time: 0.0")
    print("Synchronous Decryption Time: 0.0")

    enc_time_sync, dec_time_sync = benchmark_performance_sync(RC4_Synchronous, key, plaintext)
    print(f"Synchronous Encryption Time: {enc_time_sync}")
    print(f"Synchronous Decryption Time: {dec_time_sync}")

    rc4_async = RC4_Asynchronous(key)
    enc_time_async, dec_time_async = asyncio.run(benchmark_performance_async(rc4_async, plaintext))
    print(f"Asynchronous Encryption Time: {enc_time_async}")
    print(f"Asynchronous Decryption Time: {dec_time_async}")
