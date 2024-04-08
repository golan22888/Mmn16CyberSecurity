from crypt import encrypt_aes_cbc
from datetime import datetime


class Authenticator:
    def __init__(self, version, client_id, server_id, key):
        self.version, self.authenticator_iv = encrypt_aes_cbc(key, version, None)
        self.client_id = encrypt_aes_cbc(key, client_id, self.authenticator_iv)[0]
        server_id = bytes.fromhex(server_id)
        self.server_id = encrypt_aes_cbc(key, server_id, self.authenticator_iv)[0]
        creation_time = int(datetime.now().timestamp()).to_bytes(8, byteorder='little', signed=False)
        self.creation_time = encrypt_aes_cbc(key, creation_time, self.authenticator_iv)[0]

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
