import os
import struct
import uuid
from unittest import TestCase
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

AES_KEY_SIZE = 32
PATH = '../associated_files/msg.info'
SERVERS_MUTUAL_KEY = b'DlU/1WUMQgbfqzX+mO5QlNzUAQT7VpJUE1vfHouFO/s='
SERVERS_SECRET_KEY = b'rkeVrlQVDTKm88jaGLwnzkSgBOdGNaO61PkEPdySDKs='


class TestCrypt(TestCase):
    content = 14

    def test_all(self):
        try:
            # key = self.test_generate_aes_key()
            # key = base64.b64encode(key)
            # print(key)
            # key = base64.b64decode(key)
            key = base64.b64decode(SERVERS_MUTUAL_KEY)
            print(key)
            cipher_text, iv = self.test_encrypt_aes_cbc(key, self.content)
            print(cipher_text)
            decrypted_content = self.test_decrypt_aes_cbc(key, cipher_text, iv)
            print(decrypted_content)
        except Exception as e:
            print(e)

    def test_encrypt_aes_cbc(self, key, content):
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        if isinstance(content, int):
            content = str(content).encode('utf-8')  # Convert integer to bytes
        elif isinstance(content, bytes):
            pass  # Do nothing if plaintext is already bytes
        else:
            content = content.encode('utf-8')  # Convert string to bytes
        padded_data = pad(content, AES.block_size)
        ciphertext = cipher.encrypt(padded_data)
        print(iv, "\n", ciphertext)
        return base64.b64encode(ciphertext), base64.b64encode(iv)

    def test_decrypt_aes_cbc(self, key, ciphertext, iv):
        try:
            cipher = AES.new(key, AES.MODE_CBC, base64.b64decode(iv))
            decrypted_data = cipher.decrypt(base64.b64decode(ciphertext))
            unpadded_data = unpad(decrypted_data, AES.block_size)
            return unpadded_data.decode('utf-8')
        except Exception as e:
            print("Error decrypting data:", e)
            return None

    def test_generate_aes_key(self):
        aes_key = get_random_bytes(AES_KEY_SIZE)
        return aes_key
