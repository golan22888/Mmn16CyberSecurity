from datetime import datetime, timedelta
from crypt import encrypt_aes_cbc as crypt_cbc
from authenticator_constant import SERVER_VERSION, SERVERS_MUTUAL_KEY


class Ticket:
    def __init__(self, client_id, server_id, client_and_mag_server_aes_key):
        self.version = SERVER_VERSION
        self.client_id = client_id
        self.server_id = server_id
        creation_time = datetime.now()
        self.creation_time = datetime.now().timestamp()
        (self.encrypted_aes_key_client_and_msg_server,
         self.ticket_iv) = crypt_cbc(SERVERS_MUTUAL_KEY,
                                     client_and_mag_server_aes_key, None)
        expiration_time = (creation_time + timedelta(0, 300, 0)).timestamp()
        self.encrypted_expiration_time = crypt_cbc(SERVERS_MUTUAL_KEY, expiration_time, self.ticket_iv)[0]

    def get_version(self):
        return self.version

    def get_client_id(self):
        return self.client_id

    def get_server_id(self):
        return self.server_id

    def get_creation_time(self):
        return self.creation_time

    def get_ticket_iv(self):
        return self.ticket_iv

    def get_encrypted_aes_key(self):
        return self.encrypted_aes_key_client_and_msg_server

    def get_encrypted_expiration_time(self):
        return self.encrypted_expiration_time
