import random
from synchronous import RC4_Synchronous
from math import sqrt, erfc

def main():
  random.seed(50)
  n = 10000
  
  print(f'Running monobit frequency test for {n*8} bitstream')
  key = random.randbytes(256)
  rc4 = RC4_Synchronous(key)
  keystream = bytes(rc4.getKeystream(n))
  
  sum = 0
  
  for i in range(n*8):
    if keystream[i//8] & (1 << (i % 8)) != 0:
      sum += 1
    else:
      sum -= 1
  sum /= sqrt(n*8)
  
  print(f'p = {erfc(abs(sum)/sqrt(2)):0.9f}')
  print(f'since p > 0.01, the sequence is random')

if __name__ == '__main__':
  main()