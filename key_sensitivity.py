import random
from synchronous import RC4_Synchronous
import numpy as np

def main():
  # create a random 256 byte array key
  random.seed(50)
  for bb in range(1, 11):
    avg_init_zeros = 0
    times = 5000
    n = 2048
    num_flip_bits = bb
    for i in range(times):
      key = random.randbytes(256)
      rc4 = RC4_Synchronous(key)
      
      keystream = bytes(rc4.getKeystream(n))
      
      # randomly change bits in the key
      key = bytearray(key)
      bits_to_flip = random.sample(range(256*8), num_flip_bits)
      for b in bits_to_flip:
        key[b//8] = key[b//8] ^ (1 << (b%8))
      key = bytes(key)
      
      # get new keystream
      rc4 = RC4_Synchronous(key)
      new_keystream = bytes(rc4.getKeystream(n))
      
      xored = [x ^ y for x, y in zip(keystream, new_keystream)]
      
      total_num_bits = len(xored)*8

      def get_starting_zeros():
        for j in range(total_num_bits):
          if xored[j//8] & (1 << ((7-(j%8)))) != 0:
            return j
        return total_num_bits
      
      avg_init_zeros += get_starting_zeros()
      
    print(f'average number of same starting bits with {bb} random bit flips in the key: {avg_init_zeros/times}')
  

def calculate_set_bits(n):
  count = 0
  while n:
    count += n & 1
    n >>= 1
  return count

if __name__ == "__main__":
    main()