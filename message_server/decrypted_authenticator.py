from crypt import decrypt_aes_cbc as decrypt

SERVER_VERSION = 24


class DecryptedAuthenticator:
    def __init__(self, aes_key_client_mas_server, authenticator_iv, version, client_id, server_id, creation_time):
        self.authenticator_iv = authenticator_iv
        self.version = decrypt(aes_key_client_mas_server, version, authenticator_iv)
        self.client_id = decrypt(aes_key_client_mas_server, client_id, authenticator_iv)
        self.server_id = decrypt(aes_key_client_mas_server, server_id, authenticator_iv)
        self.creation_time = decrypt(aes_key_client_mas_server, creation_time, authenticator_iv)

    def get_authenticator_iv(self):
        return self.authenticator_iv

    def get_version(self):
        return self.version

    def get_client_id(self):
        return self.client_id

    def get_server_id(self):
        return self.server_id

    def get_creation_time(self):
        return self.creation_time
