import random
from synchronous import RC4_Synchronous
from math import sqrt, erfc

# Runs test reference: page 27 of https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-22r1a.pdf
def main():
  random.seed(50)
  n = 10000
  
  print(f'Running test test for {n*8} bitstream')
  key = random.randbytes(256)
  rc4 = RC4_Synchronous(key)
  keystream = bytes(rc4.getKeystream(n))
  
  # pretest proportion pi
  pi = 0
  for i in range(n*8):
    if keystream[i//8] & (1 << (i % 8)) != 0:
      pi += 1
  pi /= n*8
  
  print(f'pretest proportion pi = {pi:0.9f}')
  
  # test statistic
  v_obs = 0
  for i in range(n*8-1):
    if (1 if (keystream[i//8] & (1 << (7 - (i % 8)))) != 0 else 0) != (1 if (keystream[(i+1)//8] & (1 << (7 - ((i+1) % 8)))) != 0 else 0):
      v_obs += 1
  v_obs += 1  # for the last bit
  print(f'v_obs = {v_obs}')
  
  # compute p-value
  
  # set n as number of bits
  n = n*8
  
  p = erfc(abs(v_obs - 2*n*pi*(1-pi))/(2*sqrt(2*n)*pi*(1-pi)))
  
  print(f'p = {p:0.9f}')
  print(f'since p > 0.01, the sequence is random')

if __name__ == '__main__':
  main()