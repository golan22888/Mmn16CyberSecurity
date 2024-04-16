from datetime import datetime
import struct


class Client:
    def __init__(self, client_id, client_msg_server_key, expiration_time):
        self.client_id = client_id
        self.client_msg_server_key = client_msg_server_key
        if isinstance(expiration_time, bytes):
            self.expiration_time = struct.unpack('d', expiration_time)[0]
        elif isinstance(expiration_time, str):
            self.expiration_time = float(expiration_time[:-2])

    def get_client_id(self):
        return self.client_id

    def get_client_msg_server_key(self):
        return self.client_msg_server_key

    def get_expiration_time(self):
        return self.expiration_time

    def key_is_expired(self):
        return datetime.now().timestamp() > self.get_expiration_time()

    def set_expiration_time(self, expiration_time):
        self.expiration_time = expiration_time

    def set_client_msg_server_key(self, client_msg_server_key):
        self.client_msg_server_key = client_msg_server_key
