from crypt import generate_aes_key, encrypt_aes_cbc as encrypt_cbc
from client import Client


class EncryptedKey:
    def __init__(self, nonce, client_and_mag_server_aes_key, client):
        self.encrypted_nonce, self.encrypted_key_iv = encrypt_cbc(client.get_password_hash(), nonce, None)
        self.encrypted_key = encrypt_cbc(client.get_password_hash(), client_and_mag_server_aes_key,
                                         self.encrypted_key_iv)

