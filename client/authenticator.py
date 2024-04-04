from crypt import encrypt_aes_cbc


class Authenticator:
    def __init__(self, authenticator_iv, version, client_id, server_id, creation_time, key):
        self.authenticator_iv = authenticator_iv
        self.version = encrypt_aes_cbc(key, version, authenticator_iv)
        self.client_id = encrypt_aes_cbc(key, client_id, authenticator_iv)
        self.server_id = encrypt_aes_cbc(key, server_id, authenticator_iv)
        self.creation_time = encrypt_aes_cbc(key, creation_time, authenticator_iv)

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
