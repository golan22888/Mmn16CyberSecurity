import base64
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

AES_KEY_SIZE = 32


def generate_aes_key():
    aes_key = get_random_bytes(AES_KEY_SIZE)
    return aes_key


def encrypt_aes_cbc(key, plaintext, iv):
    if iv is None:
        iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(plaintext.encode('utf-8'), AES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return base64.b64encode(ciphertext), base64.b64encode(iv)
