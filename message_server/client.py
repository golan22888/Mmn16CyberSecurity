from datetime import datetime


class Client:
    def __init__(self, client_id, client_msg_server_key, expiration_time):
        self.client_id = client_id
        self.client_msg_server_key = client_msg_server_key
        self.expiration_time = expiration_time

    def get_client_id(self):
        return self.client_id

    def get_client_msg_server_key(self):
        return self.client_msg_server_key

    def get_expiration_time(self):
        return self.expiration_time

    def key_is_expired(self):
        return datetime.now() > self.get_expiration_time()
