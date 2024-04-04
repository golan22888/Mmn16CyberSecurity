from crypt import decrypt_aes_cbc


class DecryptedEncryptedKey:
    def __init__(self, encrypted_key_iv, nonce, client_and_mag_server_aes_key, key):
        self.encrypted_key_iv = encrypted_key_iv
        self.nonce = decrypt_aes_cbc(key, nonce, encrypted_key_iv)
        self.client_and_mag_server_aes_key = decrypt_aes_cbc(key, client_and_mag_server_aes_key, encrypted_key_iv)

    def get_encrypted_key_iv(self):
        return self.encrypted_key_iv

    def get_nonce(self):
        return self.nonce

    def get_client_and_mag_server_aes_key(self):
        return self.client_and_mag_server_aes_key
