from abc import ABC
from authenticator_constant import CLIENT_ID_SIZE, ENCRYPTED_KEY_SIZE, TICKET_SIZE


class Payload(ABC):
    pass


class RequestUserPayload(Payload):
    def __init__(self, name, password):
        self.name = name
        self.password = password

    def get_name(self):
        return self.name

    def get_password(self):
        return self.password


class RequestSymKeyPayload(Payload):
    def __init__(self, server_id, nonce):
        self.server_id = server_id
        self.nonce = nonce

    def get_server_id(self):
        return self.server_id

    def get_nonce(self):
        return self.nonce


class ResponseEmptyPayload(Payload):
    @staticmethod
    def get_size():
        return 0


class ResponsePayload(Payload):
    def __init__(self, client_id):
        self.client_id = client_id

    def get_client_id(self):
        return self.client_id

    def get_size(self):
        return CLIENT_ID_SIZE


class ResponseKeyPayload(ResponsePayload):
    def __init__(self, client_id, encrypted_key, ticket):
        super().__init__(client_id)
        self.encrypted_key = encrypted_key
        self.ticket = ticket

    def get_client_id(self):
        return self.client_id

    def get_encrypted_key(self):
        return self.encrypted_key

    def get_ticket(self):
        return self.ticket

    def get_size(self):
        return super().get_size() + ENCRYPTED_KEY_SIZE + TICKET_SIZE
