import matplotlib.pyplot as plt
import numpy as np
from synchronous import RC4_Synchronous
from asynchronous import RC4_Asynchronous
from tests_eval import benchmark_performance_sync, benchmark_performance_async
import asyncio


def visualize_performance(num_iterations=10):
    sync_enc_times = []
    sync_dec_times = []
    async_enc_times = []
    async_dec_times = []

    key = b"supersecretkey"
    plaintext = b"hello world"

    for _ in range(num_iterations):
        enc_time_sync, dec_time_sync = benchmark_performance_sync(RC4_Synchronous, key, plaintext)
        sync_enc_times.append(enc_time_sync)
        sync_dec_times.append(dec_time_sync)

        rc4_async = RC4_Asynchronous(key)
        enc_time_async, dec_time_async = asyncio.run(benchmark_performance_async(rc4_async, plaintext))
        async_enc_times.append(enc_time_async)
        async_dec_times.append(dec_time_async)

    sync_avg_enc_time = np.mean(sync_enc_times)
    sync_avg_dec_time = np.mean(sync_dec_times)
    async_avg_enc_time = np.mean(async_enc_times)
    async_avg_dec_time = np.mean(async_dec_times)

    # Plotting
    labels = ['Synchronous Encryption', 'Synchronous Decryption', 'Asynchronous Encryption', 'Asynchronous Decryption']
    avg_times = [sync_avg_enc_time, sync_avg_dec_time, async_avg_enc_time, async_avg_dec_time]

    plt.figure(figsize=(10, 6))
    plt.bar(labels, avg_times, color=['blue', 'blue', 'orange', 'orange'])
    plt.xlabel('Operations')
    plt.ylabel('Average Time (seconds)')
    plt.title('Average Encryption and Decryption Time ({} Iterations)'.format(num_iterations))
    plt.show()


if __name__ == "__main__":
    visualize_performance(num_iterations=1000)
