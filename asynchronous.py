import asyncio

class RC4_Asynchronous:
    def __init__(self, key):
        self.S = list(range(256))
        self.key = key

    async def KSA(self):
        j = 0
        for i in range(256):
            j = (j + self.S[i] + self.key[i % len(self.key)]) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]
            await asyncio.sleep(0)  # Yield to other tasks

    async def PRGA(self):
        i = 0
        j = 0
        while True:
            i = (i + 1) % 256
            j = (j + self.S[i]) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]
            await asyncio.sleep(0)  # Yield to other tasks
            yield self.S[(self.S[i] + self.S[j]) % 256]

    async def encrypt(self, plaintext):
        await self.KSA()
        keystream = self.PRGA()
        encrypted = bytes([x ^ await keystream.__anext__() for x in plaintext])
        return encrypted

    async def decrypt(self, ciphertext):
        return await self.encrypt(ciphertext)  # RC4 is symmetric


async def main():
    key = b"SecretKey"
    rc4 = RC4_Asynchronous(key)
    plaintext = b"Hello, World!"
    encrypted = await rc4.encrypt(plaintext)
    decrypted = await rc4.decrypt(encrypted)
    print("Plaintext:", plaintext)
    print("Encrypted:", encrypted)
    print("Decrypted:", decrypted)

if __name__ == "__main__":
    asyncio.run(main())
