class RC4_Synchronous:
    def __init__(self, key):
        self.S = list(range(256))
        self.key = key

    def KSA(self):
        self.S = list(range(256))
        j = 0
        for i in range(256):
            j = (j + self.S[i] + self.key[i % len(self.key)]) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]
    
    # for testing purposes
    def getKeystream(self, length):
        self.KSA()
        keystream = []
        i = 0
        j = 0
        for _ in range(length):
            i = (i + 1) % 256
            j = (j + self.S[i]) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]
            keystream.append(self.S[(self.S[i] + self.S[j]) % 256])
        return keystream

    def PRGA(self):
        i = 0
        j = 0
        while True:
            i = (i + 1) % 256
            j = (j + self.S[i]) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]
            yield self.S[(self.S[i] + self.S[j]) % 256]

    def encrypt(self, plaintext):
        self.KSA()
        keystream = self.PRGA()
        return bytes([x ^ next(keystream) for x in plaintext])

    def decrypt(self, ciphertext):
        return self.encrypt(ciphertext)  # RC4 is symmetric


if __name__ == "__main__":
    key = b"SecretKey"
    rc4 = RC4_Synchronous(key)
    print("Keystream:", bytes(rc4.getKeystream(20)).hex())
    plaintext = b"Hello, World!"
    encrypted = rc4.encrypt(plaintext)
    decrypted = rc4.decrypt(encrypted)
    print("Plaintext:", plaintext)
    print("Encrypted:", encrypted.hex())
    print("Decrypted:", decrypted.hex())
    # convert bytes to string
    decrypted = decrypted.decode("utf-8")
    print("Decrypted string:", decrypted)
