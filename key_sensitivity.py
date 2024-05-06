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
      
      # randomly change a bit in the key
      key = bytearray(key)
      bits_to_flip = random.sample(range(256*8), num_flip_bits)
      for b in bits_to_flip:
        key[b//8] = key[b//8] ^ (1 << (b%8))
      key = bytes(key)
      
      # key = random.randbytes(256)
      rc4 = RC4_Synchronous(key)
      new_keystream = bytes(rc4.getKeystream(n))
      
      xored = [x ^ y for x, y in zip(keystream, new_keystream)]
      
      # print the number of 1s in the xored array
      # print(f'length of key: {len(key)}, number of different bits: {sum([calculate_set_bits(x) for x in xored if x != 1])}')
      
      # print hex of first 10 bytes of encrypted and new_encrypted
      # print(f'encrypted: {encrypted[:10].hex()}')
      # print(f'new_encrypted: {new_encrypted[:10].hex()}')
      # print(f'xored: {bytes(xored[:10]).hex()}')
      
      # print(f'lenght of xored: {len(xored)}')
      
      # look at each sequence of 8 bits (b0..b7, b1..b8, b2..b9) as a number and increment the appropriate counter in the array
      # xored = bytearray(random.randbytes(n))
      # xored[0] = 0b00000111
      # xored[1] = 0b01010000
      # xored = bytes(xored)
      total_num_bits = len(xored)*8
      
      # def get_num(i):
      #   num = 0
      #   for j in range(8):
      #     num <<= 1
      #     num |= 1 if xored[(i+j)//8] & (1 << ((7-((i+j)%8)))) != 0 else 0
      #   assert num < 256
      #   return num

      def get_starting_zeros():
        for j in range(total_num_bits):
          if xored[j//8] & (1 << ((7-(j%8)))) != 0:
            return j
        return total_num_bits
      
      # freq_array = [0]*256
      # for x in range(total_num_bits-8):
      #   freq_array[get_num(x)] += 1
      
      # freq_array = np.array(freq_array)
      # assert sum(freq_array) == total_num_bits-8
      # range_array = np.array(range(256))
      # std = np.repeat(range_array, freq_array).std()
      
      # print(f'rand value: {(std*256)/(n*8)}')
      # print(f'init zeros: {get_init_zeros()}')
      
      avg_init_zeros += get_starting_zeros()
      # print(f'rand value: {std}')
      
      # print(f'frequency of different bits: {freq_array}')
      
    print(f'average number of same starting bits with {bb} random bit flips in the key: {avg_init_zeros/times}')
  

def calculate_set_bits(n):
  count = 0
  while n:
    count += n & 1
    n >>= 1
  return count

if __name__ == "__main__":
    main()