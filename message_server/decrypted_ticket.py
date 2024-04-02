from datetime import datetime, timedelta
from crypt import decrypt_aes_cbc as decrypt

SERVERS_MUTUAL_KEY = 'DlU/1WUMQgbfqzX+mO5QlNzUAQT7VpJUE1vfHouFO/s'

SERVER_VERSION = 24


class DecryptedTicket:
    def __init__(self, version, client_id, server_id, creation_time, ticket_iv, encrypted_client_and_msg_server_aes_key,
                 encrypted_expiration_time):
        self.version = version
        self.client_id = client_id
        self.server_id = server_id
        self.creation_time = creation_time
        self.ticket_iv = ticket_iv
        self.decrypted_client_and_msg_server_aes_key = decrypt(SERVERS_MUTUAL_KEY,
                                                               encrypted_client_and_msg_server_aes_key, self.ticket_iv)
        self.decrypted_expiration_time = decrypt(SERVER_VERSION, encrypted_expiration_time, self.ticket_iv)

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

    def get_decrypted_client_and_msg_server_aes_key(self):
        return self.decrypted_client_and_msg_server_aes_key

    def get_decrypted_expiration_time(self):
        return self.decrypted_expiration_time

    def is_expired(self):
        return datetime.now() > self.decrypted_expiration_time
