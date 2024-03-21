import base64
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

AES_KEY_SIZE = 16
IV = b'\x00' * 16


class Crypt:
    @staticmethod
    def generate_aes_key():
        aes_key = get_random_bytes(AES_KEY_SIZE)
        return aes_key

    @staticmethod
    def encrypt_aes_cbc(key, plaintext, iv):
        if iv is None:
            iv = get_random_bytes(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_data = pad(plaintext, AES.block_size)
        ciphertext = cipher.encrypt(padded_data)
        return base64.b64encode(ciphertext), base64.b64encode(iv)

