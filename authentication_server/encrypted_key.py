from crypt import encrypt_aes_cbc as encrypt_cbc


class EncryptedKey:
    def __init__(self, nonce, client_and_mag_server_aes_key, client):
        self.encrypted_nonce, self.encrypted_key_iv = encrypt_cbc(client.get_password_hash(), nonce, None)
        self.encrypted_key = encrypt_cbc(client.get_password_hash(), client_and_mag_server_aes_key,
                                         self.encrypted_key_iv)

    def get_encrypted_key_iv(self):
        return self.encrypted_key_iv

    def get_nonce(self):
        return self.encrypted_nonce

    def get_encrypted_key(self):
        return self.encrypted_key

