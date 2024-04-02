import struct
import uuid
from unittest import TestCase
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from struct import pack, unpack
from authentication_server.client import Client
from authentication_server.clients_manager import ClientsManager
from datetime import datetime

from authentication_server.payload_serializer import RequestSymKeyPayloadSerializer

AES_KEY_SIZE = 32
PATH = '../associated_files/msg.info'

class TestCrypt(TestCase):
    content = "avihu"

    # def test_all(self):

        # print(base64.b64encode(key))
        # cipher_text, iv = self.test_encrypt_aes_cbc(key, self.content)
        # print(cipher_text)
        # decrypted_content = self.test_decrypt_aes_cbc(key, cipher_text, iv)
        # print(decrypted_content)

    def test_encrypt_aes_cbc(self, key, content):
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_data = pad(content.encode('utf-8'), AES.block_size)
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

    def test_encrypt_aes_key(self):
        client_id = uuid.uuid4().hex
        name = "avihu"
        password_hash = ClientsManager.sha256_digest("8614523")
        last_seen = datetime.now()
        client = Client(client_id, name, password_hash, last_seen)
        # print(ticket)
        # print(key, '\n', client_id, '\n', server_id, '\n' )
        protocol_payload_format = f'< {97}s'
        # ticket_packed = struct.pack(protocol_payload_format, ticket)
        # ticket_unpacked = struct.unpack(protocol_payload_format, ticket_packed)
        # ticket_unpacked.
        # ticket2 = Ticket(ticket_unpacked[0])
